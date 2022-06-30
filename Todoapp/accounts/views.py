from django.contrib.auth import views as auth_views
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from memberships.views import getuser_membership, get_user_subscription

#from .decorators import unauthenticated_user

# Create your views here.
from .models import *
from .forms import *




class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('login')


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'


def logoutUser(request):
  logout(request)
  return redirect('login')


@login_required
def profilepage(request):
    user_plan  = getuser_membership(request)
    user_subscription = get_user_subscription(request)

    context = {
        'email': request.user.email,
        'plan':user_plan,
        'user_subscription': user_subscription
    }
    return render(request ,"user/profile.html", context)