from django.shortcuts import render,redirect, get_object_or_404
from .forms import WorkForm, CreateUserForm
from .models import Work
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'ToDoApp/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'ToDoApp/signup.html', {'form' : CreateUserForm()})
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                username = user.cleaned_data.get('username')
                messages.success(request, f'Welcome , { username } Your Account is been created!')
                return redirect('login')
            except IntegrityError:
                return render(request, 'ToDoApp/signup.html', {'form':CreateUserForm(), 'error': 'That username has already been taken. Please choose a new username'})
            
        else:
            return render(request, 'ToDoApp/signup.html', {'form':CreateUserForm(), 'error': 'Passwords did not match'})
        
@login_required       
def loginuser(request):
    if request.method== 'GET':
        return render(request, 'ToDoApp/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ToDoApp/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')
        

@login_required 
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'ToDoApp/createtodo.html', {'form':WorkForm()})
    else:
        try:
            form = WorkForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'ToDoApp/createtodo.html', {'form': WorkForm(), 'error':'Bad data passed in, Try Again:('})
        

@login_required 
def currentuser(request):
    todos = Work.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'ToDoApp/currentuser.html', {'todos':todos})


@login_required 
def completedtodo(request):
    todos = Work.objects.filter(user=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'ToDoApp/completedtodo.html', {'todos':todos})


@login_required 
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Work, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = WorkForm(instance=todo)
        return render(request, 'ToDoApp/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = WorkForm(request.POST, instance=todo)
            form.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'ToDoApp/viewtodo.html', {'todo':todo, 'form':form, 'error': 'Bad info!'})


@login_required 
def completetodo(request,todo_pk):
    todo = get_object_or_404(Work, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed = timezone.now()
        todo.save()
        return redirect('currentuser')


@login_required     
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Work, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentuser')
