from django.shortcuts import render
from django.http import HttpResponse

def postbulletin(request):
	return HttpResponse('This is where you will post a bulletin.')