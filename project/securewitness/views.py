import uuid

from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User

from models import Bulletin, File, Permission, Folder
from users import retrieve_user_state, signup_user
from files import encrypt, decrypt
from search import search

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
    bulletin_list = Bulletin.objects.filter(encrypted=False)
    # folder_list = Folder.objects.all()
    # context['folder_list'] = folder_list
    if request.user.is_authenticated():
        permissions = Permission.objects.filter(user=request.user)
        for permission in permissions:
            bulletin_list |= Bulletin.objects.filter(pk=permission.bulletin.pk)
    context['bulletin_list'] = bulletin_list.order_by('-pub_date')
    if request.method == 'POST':
        if 'search' in request.POST:
            search_field = request.POST.get('description', '')
            context['bulletin_list'] = search(search_field)
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
    	folder_list = Folder.objects.all()
    	context['folder_list'] = folder_list
        if request.method == 'POST':
            new_bulletin = Bulletin(author=request.user, pub_date=timezone.now(), 
                                    description=request.POST['description'], 
                                    location=request.POST['location'],
                                    encrypted='encrypted' in request.POST)
            new_bulletin.save()
            key = uuid.uuid4()
            for f in request.FILES.getlist('files'):
                new_file = File(bulletin=new_bulletin, name=f.name, encryption_key=key.hex, content_type=f.content_type)
                new_file.save()
                with open('securewitness/files/' + str(new_file.id) + 
                          '_' + f.name, 'wb') as dst:
                    encrypt(f, dst, key)
            new_permission = Permission(user=request.user, bulletin=new_bulletin)
            new_permission.save()
            for user in request.POST['permissions'].split(','):
            	user = user.strip()
            	u = User.objects.filter(username=user)
            	if len(u) > 0:
            		new_permission = Permission(user=u[0], bulletin=new_bulletin)
            		new_permission.save()
            return render(request, 'securewitness/bulletinposted.html', context)
    return render(request, 'securewitness/postbulletin.html', context)


def download(request, fname):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../../signup/')
    else:
        f_id = fname.split('_')[0]
        f_name = fname.split('_')[1]
        files = File.objects.filter(id=f_id, name=f_name)
        if len(files) > 0:
            file_obj = files[0]
            file_bulletin = file_obj.bulletin
            dst = open(file_obj.name, 'wbr')
            print Permission.objects.filter(bulletin=file_bulletin)
            has_permission = len(Permission.objects.filter(bulletin=file_bulletin, user=request.user)) > 0 or not file_bulletin.encrypted
            if has_permission:
                with open('securewitness/files/' + fname, 'r') as f:
                    decrypt(f, dst, uuid.UUID(file_obj.encryption_key))
                    dst = open(file_obj.name, 'r')
                    response = HttpResponse(dst, content_type=file_obj.content_type)
                    response['Content-Disposition'] = 'attachment; filename=' + f_name
                    return response
            else:
                return render(request, 'securewitness/nopermission.html', context)
