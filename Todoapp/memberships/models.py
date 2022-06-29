from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

MEMBERSHIP_CHOICES = (
    ('Professional', 'pro'),
    ('Professional+', 'pro+'),
    ('Free', 'free')
)

PAYMENT_TYPE = (
    ('Monthly', 'monthly'),
    ('Yearly', 'yearly')
)

# Create your models here.
class Membership(models.Model):
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    price = models.IntegerField(default=0)
    payment_type= models.CharField(choices= PAYMENT_TYPE, default='Monthly', max_length= 50)
    stripe_price_id = models.CharField(max_length=200, default="price_1LCfzGHbrOhTO2jzGrkrAkqm")

    def __str__(self):
        return self.membership_type + " " + self.payment_type

class UserMembership(models.Model):
    user  = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id =models.CharField(max_length=40)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return self.user.email


#when a new user is created also make a new usermemship model and strip customer
def create_userMembership(sender, instance, created , **kwargs):
    user_membership, created = UserMembership.objects.get_or_create(
        user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        free_membership = Membership.objects.get(membership_type='Free')
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.membership = free_membership
        user_membership.save()

post_save.connect(create_userMembership, sender=settings.AUTH_USER_MODEL)



class UserSubsription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    
    def __str__(self):
        return self.stripe_subscription_id 