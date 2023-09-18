from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def home(request):
    return render(request,'ToDoApp/home.html')

def signupuser(request):
    #localhost:8000/SignUp/
    if request.method == 'GET':
        return render(request,'ToDoApp/signup.html', {'form' : UserCreationForm()})
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('loginuser')
            except IntegrityError:
                return render(request, 'ToDoApp/signup.html', {'form':UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
            
        else:
            return render(request, 'ToDoApp/signup.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})
        
def loginuser(request):
    if request.method== 'GET':
        return render(request, 'ToDoApp/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ToDoApp/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentuser')
        
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
        

def currentuser(request):
    return render(request, 'ToDoApp/currentuser.html')