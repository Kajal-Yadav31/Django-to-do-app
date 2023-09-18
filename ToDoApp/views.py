from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import WorkForm
from .models import Work
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
        

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'ToDoApp/createtodo.html', {'form': WorkForm()})
    else:
        try:
            form = WorkForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'ToDoApp/createtodo.html', {'form': WorkForm(), 'error':'Bad data passed in, Try Again:('})
        

def currentuser(request):
    todos = Work.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'ToDoApp/currentuser.html', {'todos':todos})