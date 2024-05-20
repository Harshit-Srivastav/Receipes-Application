from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.

def login_page(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if not(username and password):
            messages.error(request, 'All Fields are required')
            return redirect('/login/')
        user = User.objects.filter(username = username)
    
        if len(user) == 0:
          messages.error(request, 'User not exists')
          return redirect('/login/')
        user = authenticate(username = username, password = password) 
        print(user)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            print('doing login')
            login(request, user)
            return redirect('/receipe/')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not(first_name and last_name and username and email and password):
            messages.error(request, 'All Fields are required')
            return redirect('/register/')
        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username already exists.")
            return redirect('/register/')
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password)
        user.save()
        messages.info(request, "Account created successfully.")
        return redirect('/register/')
    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')
    