from django.shortcuts import render, redirect, get_object_or_404
from .forms import WorkForm, CreateUserForm
from .models import Work
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def home(request):
    return render(request, 'ToDoApp/home.html')


def signupuser(request):
    # localhost:8000/SignUp/
    if request.method == 'GET':
        return render(request, 'ToDoApp/signup.html', {'form': CreateUserForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                messages.success(request, 'Your Account is been created ')
                login(request, user)
                return redirect('loginuser')
            except IntegrityError:
                return render(request, 'ToDoApp/signup.html', {'form': CreateUserForm(), 'error': 'That username has already been taken. Please choose a new username'})

        else:
            return render(request, 'ToDoApp/signup.html', {'form': CreateUserForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'ToDoApp/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Invalid login credentials')
            return render(request, 'ToDoApp/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentuser')


@login_required
def logoutuser(request):
    auth.logout(request)
    messages.success(request, 'You are logged out! Wanna LogIn Again')
    return redirect('loginuser')


@login_required
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
            return render(request, 'ToDoApp/createtodo.html', {'form': WorkForm(), 'error': 'Bad data passed in, Try Again:('})


@login_required
def currentuser(request):
    todos = Work.objects.filter(user=request.user, completed__isnull=True)

    return render(request, 'ToDoApp/currentuser.html', {'todos': todos})


@login_required
def completedtodo(request):
    todos = Work.objects.filter(
        user=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'ToDoApp/completedtodo.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Work, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = WorkForm(instance=todo)
        return render(request, 'ToDoApp/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = WorkForm(request.POST, instance=todo)
            form.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'ToDoApp/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info!'})


@login_required
def completetodo(request, todo_pk):
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


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Reset your Password'
            message = render_to_string('ToDoApp/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'Password reset email has been sent to your email address.')
            return redirect('loginuser')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'ToDoApp/forgotPassword.html')


def reset_password_validate(request,  uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('loginuser')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('loginuser')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'ToDoApp/resetPassword.html')
