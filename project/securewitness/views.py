from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.utils import timezone

from models import Bulletin, File
from users import retrieve_user_state, signup_user

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
	if context['sign_up']:
		return HttpResponseRedirect('../signup/')
	else:
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
                        form = BulletinForm(request.POST, request.FILES)
                        if form.is_valid():
                                newBulletin = Bulletin(author=request.user, pub_date=timezone.now(), 
                                                       description=form.cleaned_data['description'], 
                                                       location=form.cleaned_data['location'])
                                newBulletin.save()
                                bulletinFile = File(bulletin=newBulletin, name=request.FILES['files'].name)
                                bulletinFile.save()
                                f = request.FILES['files']
                                with open('securewitness/files/' + str(bulletinFile.id) + 
                                          '_' + request.FILES['files'].name, 'wb') as destination:
                                        for chunk in f.chunks():
                                                destination.write(chunk)
                                return render(request, 'securewitness/bulletinposted.html', context)
                        else:
                                form = BulletinForm()
                        context['form'] = form
                return render(request, 'securewitness/postbulletin.html', context)
