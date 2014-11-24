from models import Bulletin
from users import retrieve_user_state
from django.shortcuts import render
from django.http import HttpResponseRedirect

def search(request):
    	context = retrieve_user_state(request)
    	bulletin_list = Bulletin.objects.all()
    	results = []
    	if bulletin_list is not None and len(bulletin_list) > 0:
    		results = bulletin_list.filter(field in Bulletin.description)
        context['results'] = results
    	return render(request, 'searchresults.html', context)
