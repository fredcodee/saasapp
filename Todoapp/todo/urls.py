from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('add/', views.addTask, name= 'add'),
  path('check/', views.checkTask, name= 'check'),
  path('delete/', views.DeleteTask, name='delete')
  
    
]