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

    # reset password.
    path('forgotPassword/', user_views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/',
         user_views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', user_views.resetPassword, name='resetPassword'),



    # path('password-reset/', auth_views.PasswordResetView.as_view(
    #     template_name='ToDoApp/password_reset.html'), name='password_reset'),

    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='ToDoApp/password_reset_done.html'), name='password_reset_done'),

    # path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='ToDoApp/password_reset_confirm.html'), name='password_reset_confirm'),

    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='ToDoApp/password_reset_complete.html'), name='password_reset_complete'),
]
