from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import (Membership,UserSubsription, UserMembership)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import stripe
from django.contrib.auth import get_user_model


stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.

#get current user membership
def getuser_membership(request):
    getmem = UserMembership.objects.filter(user = request.user)
    if getmem.exists():
        return getmem.first()
    else:
        return None

#get current user subcription
def get_user_subscription(request):
    user_subscription_qs = UserSubsription.objects.filter(
        user_membership=getuser_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
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


def upgradeplan(request, plan):
    new_membership_plan = Membership.objects.get(membership_type = plan)
    if getuser_membership(request).membership != new_membership_plan:
        session =stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email = request.user.email,
                line_items=[
                    {
                        "price": new_membership_plan.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url= request.build_absolute_uri(reverse('payment_successful'))+ '?session_id={CHECKOUT_SESSION_ID',
                cancel_url= request.build_absolute_uri(reverse('cancel'))
            )

        context={
            'membership':new_membership_plan,
            'session_id': session.id,
            'stripe_public_key':settings.STRIPE_PUBLIC_KEY
        }
    
        return render(request, 'payment.html', context)

    messages.error(request, 'you are already subscribed to this plan!')
    return redirect('profile')

def paymentsuccessful(request):
    return render(request, 'sucess.html')


def cancel(request):
    return render(request, "cancel.html")

@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event after payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']


        #retrieve stripe subscription
        customer_email = session["customer_details"]["email"]
        user_subscription_id  = session['subscription']
        sub = stripe.Subscription.retrieve( user_subscription_id)
        customer_id = sub["customer"]
        sub_price_id = sub["items"]['data'][0]['price']['id']


        membership = Membership.objects.get(stripe_price_id = sub_price_id)

        user = get_user_model().objects.get(
            email=customer_email,
        )
        user_membership = UserMembership.objects.get(user = user)
        #if there is an exiting subscription /customer deactive n delete it on stripe
        try:
            stripe.Customer.delete(user_membership.stripe_customer_id)
        except:
            pass

        user_membership.stripe_customer_id = customer_id
        user_membership.membership = membership
        user_membership.save()


        new_sub, created = UserSubsription.objects.get_or_create(
        user_membership = user_membership)
        new_sub.stripe_subscription_id = user_subscription_id
        new_sub.active = True
        new_sub.save()
            



        #send sucess email
    # Passed signature verification
    return HttpResponse(status=200)


#cancel subscription
def cancel_subscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return redirect('profile')

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type='Free')
    user_membership = getuser_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    messages.info(
        request, "Successfully cancelled membership. We have sent an email")
    # sending an email here
    return redirect('profile')



#check if subscribtion is active in stripe
@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = UserSubsription.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.save()
    return HttpResponse('completed')