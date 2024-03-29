import uuid
import datetime

from datetime import date, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from os import remove

from models import Bulletin, File, Permission, Folder, Filing
from users import retrieve_user_state, signup_user
from files import encrypt, decrypt
from search import search

# Classes
# **********
'''
class BulletinForm(forms.Form):
    description = forms.CharField(label='Description', max_length=512)
    location = forms.CharField(label='Location', max_length=256)
    files = forms.FileField(label='Files')
'''

# Views
# **********
def index(request):
    context = retrieve_user_state(request)
    context['not_fire_fox'] = request.META['HTTP_USER_AGENT'] != 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0'
    bulletin_list = Bulletin.objects.filter(encrypted=False)
    folder_list = Folder.objects.none()
    if request.user.is_authenticated():
        folder_list = Folder.objects.filter(owner=request.user)
        permissions = Permission.objects.filter(user=request.user)
        for permission in permissions:
            bulletin_list |= Bulletin.objects.filter(pk=permission.bulletin.pk)
    context['bulletin_list'] = bulletin_list.order_by('-pub_date')
    if request.method == 'POST':
        if 'search' in request.POST:
            search_field = request.POST.get('description', '')
            context['bulletin_list'] = search(search_field, None if not request.user.is_authenticated() else request.user)
        elif 'create_folder' in request.POST:
            folder_name = request.POST.get('folder', '')
            if folder_name == '':
                context['empty_folder_name'] = True
            elif len(Folder.objects.filter(owner=request.user).filter(name=folder_name)) > 0:
                context['duplicate_folder'] = True
            else:
                folder = Folder(owner=request.user, name=folder_name)
                folder.save()
        else:
            for bulletin in bulletin_list:
                if 'create_folder_move_bulletin_' + str(bulletin.pk) in request.POST:
                    folder_name = request.POST.get('folder', '')
                    if folder_name == '':
                        context['empty_folder_name'] = True
                    elif len(Folder.objects.filter(owner=request.user).filter(name=folder_name)) > 0:
                        context['duplicate_folder'] = True
                    else:
                        folder = Folder(owner=request.user, name=folder_name)
                        folder.save()
                        filing = Filing(folder=folder, bulletin=bulletin)
                        filing.save()
                    break
            for folder in folder_list:
                if 'rename_folder_' + str(folder.pk) in request.POST:
                    new_name = request.POST.get('folder', '')
                    if new_name == '':
                        context['empty_folder_name'] = True
                    elif len(Folder.objects.filter(owner=request.user).filter(name=new_name)) > 0:
                        context['duplicate_folder'] = True
                    else:
                        folder.name = new_name
                        folder.save()
                    break
                if 'folder_' + str(folder.pk) in request.POST:
                    # context['active_folder'] = {'folder_'+str(folder.pk): True}
                    context['bulletin_list'] = folder.bulletin_list().order_by('-pub_date')
                    break
    context['folder_list'] = folder_list.order_by('name')
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
    	folder_list = Folder.objects.filter(owner=request.user).order_by('name')
    	context['folder_list'] = folder_list
        if request.method == 'POST':
            new_bulletin = Bulletin(author=request.user, pub_date=timezone.now(), 
                                    description=request.POST['description'], 
                                    location=request.POST['location'],
                                    encrypted='encrypted' in request.POST)
            new_bulletin.save()
            if len(folder_list) > 0:
                folder_name = request.POST['folders']
                if folder_name != 'None':
                    new_filing = Filing(folder=Folder.objects.filter(name=folder_name, owner=request.user)[0], bulletin=new_bulletin)
                    new_filing.save()
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


def move_bulletin(request, folder_id, bulletin_id):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../../../signup/')
    else:
        filing = Filing(folder=Folder.objects.get(pk=folder_id), bulletin=Bulletin.objects.get(pk=bulletin_id))
        filing.save()
        return HttpResponseRedirect('../../..')


def copy_bulletin(request, b_id):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../../../signup/')
    else:
        new_bulletin = Bulletin.objects.get(id=b_id)
        new_bulletin.id = None
        new_bulletin.pub_date = timezone.now()
        new_bulletin.author = request.user
        new_bulletin.save()

        files = File.objects.filter(bulletin=Bulletin.objects.get(id=b_id))
        for f in files:
            old_file = open('securewitness/files/' + str(f.id) + '_' + f.name, 'r')
            new_file = f
            new_file.bulletin = new_bulletin
            new_file.id = None
            new_file.save()
            with open('securewitness/files/' + str(new_file.id) + 
                      '_' + f.name, 'wb') as dst:
                encrypt(old_file, dst, uuid.UUID(f.encryption_key))
            old_file.close()
        for permission in Permission.objects.filter(bulletin=Bulletin.objects.get(id=b_id)):
            permission.id = None
            permission.bulletin = new_bulletin
            permission.save()
        return HttpResponseRedirect('../../..')


def delete_bulletin(request, b_id):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../../../signup/')
    else:
        old_bulletin = Bulletin.objects.get(id=b_id)
        files = File.objects.filter(bulletin=Bulletin.objects.get(id=b_id))
        for f in files:
            remove('securewitness/files/' + str(f.id) + '_' + f.name)
            f.delete()
        old_bulletin.delete()
        return HttpResponseRedirect('../../..')


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
                    remove(file_obj.name)
                    return response
            else:
                return render(request, 'securewitness/nopermission.html', context)


def copy_folder(request, folder_id):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../../../signup/')
    else:
        folder = Folder.objects.get(pk=folder_id)
        folder_copy = Folder(owner=request.user, name='Copy of '+folder.name)
        folder_copy.save()
        return HttpResponseRedirect('../../..')


def delete_folder(request, folder_id):
    context = retrieve_user_state(request)
    if not context['logged_in']:
        return HttpResponseRedirect('../../../signup/')
    else:
        folder = Folder.objects.get(pk=folder_id)
        folder.delete()
        return HttpResponseRedirect('../../..')
