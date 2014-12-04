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
    	for entry in bulletin_list:
            if entry not in results:
                if field.lower() in entry.author.get_username().lower() or field.lower() in entry.location.lower() or field.lower() in entry.description.lower():
                    results.append(entry)
    return results
