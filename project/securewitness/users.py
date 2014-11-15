from django.contrib.auth import authenticate, login, logout


def retrieve_user_state(request):
    context = { 'username' : None , 
                'logged_in' : False ,
                'invalid_login' : False, 
                'sign_up' : False }
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
        elif 'signup' in request.POST:
            # send user to sign up page
            context['sign_up'] = True
    if 'logout' not in request.POST and request.user.is_authenticated():
        context['username'] = request.user.username
    if context['username'] is not None:
        context['logged_in'] = True
    return context
