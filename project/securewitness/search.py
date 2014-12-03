from models import Bulletin, Permission
from users import retrieve_user_state
from django.shortcuts import render
from django.http import HttpResponseRedirect
from itertools import chain

def search(field, user):
    results = []
    bulletin_list = Bulletin.objects.filter(encrypted=False)
    if user is None:
        permissions = []
    else:
        permissions = Permission.objects.filter(user=user)
    for permission in permissions:
        bulletin_list |= Bulletin.objects.filter(pk=permission.bulletin.pk)
    if bulletin_list is not None and len(bulletin_list) > 0:
    	desc_match = bulletin_list.filter(description=field)
    	auth_match = bulletin_list.filter(author__username=field)
    	loc_match = bulletin_list.filter(location=field)
    	results = list(chain(desc_match, auth_match, loc_match))
    return results
