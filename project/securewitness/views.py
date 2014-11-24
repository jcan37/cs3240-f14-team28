import uuid

from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.utils import timezone

from models import Bulletin, File, Permission
from users import retrieve_user_state, signup_user
from files import encrypt

# Classes
# **********
class BulletinForm(forms.Form):
    description = forms.CharField(label='Description', max_length=512)
    location = forms.CharField(label='Location', max_length=256)
    files = forms.FileField(label='Files')


# Views
# **********
def index(request):
    context = retrieve_user_state(request)
    if request.user.is_authenticated():
        bulletin_list = Bulletin.objects.filter(author=request.user)
        print bulletin_list
        context['bulletin_list'] = bulletin_list
    return render(request, 'securewitness/index.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        if 'signup' in request.POST:
            # sign user up
            context.update(signup_user(request))
            if not (context['fields_blank'] or 
                    context['user_exists'] or 
                    context['password_mismatch']):
                return HttpResponseRedirect('..')
        elif 'login' in request.POST:
            # sign user in
            context.update(retrieve_user_state(request))
            if context['logged_in']:
                return HttpResponseRedirect('..')
    return render(request, 'securewitness/signup.html', context)


def post(request):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../signup/')
    else:
        if request.method == 'POST':
            new_bulletin = Bulletin(author=request.user, pub_date=timezone.now(), 
                                   description=request.POST['description'], 
                                   location=request.POST['location'])
            new_bulletin.save()
            key = uuid.uuid4()
            for f in request.FILES.getlist('files'):
                new_file = File(bulletin=new_bulletin, name=f.name, encryption_key=key.hex)
                new_file.save()
                with open('securewitness/files/' + str(new_file.id) + 
                          '_' + request.FILES['files'].name, 'wb') as dst:
                    encrypt(f, dst, key)
                new_permission = Permission(user=request.user, file=new_file)
                new_permission.save()
            return render(request, 'securewitness/bulletinposted.html', context)
    return render(request, 'securewitness/postbulletin.html', context)

def download(request, fname):
	context = retrieve_user_state(request)
	if not context['logged_in']:
		return HttpResponseRedirect('../signup/')
	else:
		has_permission = True
		if has_permission:
			Files.objects.filter(name=fname)
