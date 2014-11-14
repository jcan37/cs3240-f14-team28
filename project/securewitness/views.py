from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# from django.core.context_processors import csrf
from django.utils import timezone
from models import Bulletin, File

# Classes
# **********
class BulletinForm(forms.Form):
	description = forms.CharField(label='Description', max_length=512)
	location = forms.CharField(label='Location', max_length=256)
	files = forms.FileField(label='Files')


# Views
# **********
def index(request):
        context = {'username' : None , 'logged_in' : False ,'invalid_login' : False}
        if request.method == 'POST':
                if 'login' in request.POST:
                        # Sign user in
                        username = request.POST.get('username', '')
                        password = request.POST.get('password', '')
                        user = authenticate(username=username, password=password)
                        if user is not None:
                                login(request, user)
                                context['username'] = user.username
                        else:
                                context['invalid_login'] = True
                elif 'logout' in request.POST:
                        # Sign user out
                        logout(request)
                        context['username'] = None
        if 'logout' not in request.POST and request.user.is_authenticated():
                context['username'] = user.username
        if context['username'] is not None:
                context['logged_in'] = True
        return render(request, 'securewitness/index.html', context)


def postbulletin(request):
	if request.method == 'POST':
		form = BulletinForm(request.POST, request.FILES)
		if form.is_valid():
			newBulletin = Bulletin(author=request.user, pub_date=timezone.now(), description=form.cleaned_data['description'], location=form.cleaned_data['location'])
			newBulletin.save()
			bulletinFile = File(bulletin=newBulletin, name=request.FILES['files'].name)
			bulletinFile.save()
			f = request.FILES['files']
			with open('securewitness/files/' + str(bulletinFile.id) + '_' + request.FILES['files'].name, 'wb') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
			return render(request, 'securewitness/bulletinposted.html')
	else:
		form = BulletinForm()
	return render(request, 'securewitness/postbulletin.html', {'form': form})
