from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django import forms
from django.shortcuts import render
from django.utils import timezone
from models import Bulletin, File

# Classes
# **********
class BulletinForm(forms.Form):
	description = forms.CharField(label='Description', max_length=1000)
	location = forms.CharField(label='Location', max_length=200)
	files = forms.FileField(label='Files')


# Views
# **********
def login(request):
        return HttpResponse('Login page')


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


def index(request):
	return render(request, 'securewitness/index.html')
