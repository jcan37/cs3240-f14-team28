from models import Bulletin
from users import retrieve_user_state
from django.shortcuts import render
from django.http import HttpResponseRedirect

def search(field, author, year):
    	bulletin_list = Bulletin.objects.all()
    	results = []
    	if bulletin_list is not None and len(bulletin_list) > 0:
    		results = bulletin_list.filter(description=field)
        return results
