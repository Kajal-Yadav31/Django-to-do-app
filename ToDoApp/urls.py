from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.createtodo, name='createtodo'),
    path('Currentuser/', views.currentuser, name='currentuser'),
    path('completed/', views.completedtodo, name='completedtodo'),
    path('todo/<int:todo_pk>/', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete/', views.deletetodo, name='deletetodo'),
]
