from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def retrieve_user_state(request):
    context = { 'username' : None , 
                'logged_in' : False ,
                'invalid_login' : False }
    if request.method == 'POST':
        if 'login' in request.POST:
            # sign user in
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                # valid user
                login(request, user)
                context['username'] = user.username
            else:
                # invalid user
                context['invalid_login'] = True
        elif 'logout' in request.POST:
            # sign user out
            logout(request)
            context['username'] = None
    if 'logout' not in request.POST and request.user.is_authenticated():
        context['username'] = request.user.username
    if context['username'] is not None:
        context['logged_in'] = True
    return context


def signup_user(request):
    context = { 'fields_blank' : False ,
                'user_exists' : False ,
                'password_mismatch' : False }
    email = request.POST.get('email', '')
    username = request.POST.get('new_username', '')
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    if email == '' or username == '' or password1 == '' or password2 == '':
        context['fields_blank'] = True
        return context
    if User.objects.filter(username=username).count():
        context['user_exists'] = True
        return context
    if password1 != password2:
        context['password_mismatch'] = True
        return context
    user = User.objects.create_user(username, email, password1)
    user.save()
    user = authenticate(username=username, password=password1)
    login(request, user)
    return context
