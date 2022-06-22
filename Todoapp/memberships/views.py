from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import (Membership,UserSubsription, UserMembership)
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.

def getuser_membership(request):
    getmem = UserMembership.objects.filter(user = request.user)
    if getmem.exists():
        return getmem.first()
    else:
        return None



@login_required(login_url='login')
def viewPlans(request):
    membership = Membership.objects.all()
    current_membership= getuser_membership(request)
    
    context = {
        'memberships': membership,
        'current_membership': current_membership
    }
    return render(request, 'plans.html', context)


def upgradeplan(request):
    if request.method  == "POST":
        new_userMembership = request.POST['membership_type']

        #split because we get both plan and time recurring
        new_userMembership = new_userMembership.split(" ")
        new_userMembership_plan = new_userMembership[0] #plan name
        new_user_recurringTime = new_userMembership[-1] #monthly or yearly


    return render (request, 'payment.html')
