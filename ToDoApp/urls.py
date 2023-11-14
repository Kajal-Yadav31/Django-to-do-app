from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', user_views.home, name='home'),
    path('create/', user_views.createtodo, name='createtodo'),
    path('Currentuser/', user_views.currentuser, name='currentuser'),
    path('completed/', user_views.completedtodo, name='completedtodo'),
    path('todo/<int:todo_pk>/', user_views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete',
         user_views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete/', user_views.deletetodo, name='deletetodo'),
    # Authentication
    path('SignUp/', user_views.signupuser, name="signupuser"),
    path('LogIn/', user_views.loginuser, name="loginuser"),
    path('LogOut/', user_views.logoutuser,
         name="logoutuser"),

]
