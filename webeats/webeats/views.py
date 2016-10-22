from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login

def index(request):
    return render(request, 'index.html',)

def login_view(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    message = None
    if username is not None and password is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                message = 'Account suspended'
            return render(request, 'profiles/login.html', {'message': message})
        else:
            message = 'Login unsuccessfull'
    return render(request, 'profiles/login.html', {'message': message}) 

def logout_view(request):
    logout(request)
    return redirect('index')
