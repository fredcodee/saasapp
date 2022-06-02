from django.urls import path
from . import views
from .views import LoginView, RegisterView


urlpatterns = [
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/',views.logoutUser, name = 'logout'),

    
]

