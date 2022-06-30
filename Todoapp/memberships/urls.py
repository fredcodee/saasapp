from django.urls import path
from . import views

urlpatterns = [
    path("viewplans/", views.viewPlans, name='view_plans'),
    path('upgradeplan/<str:plan>/', views.upgradeplan, name ="upgrade_plan"),
    path('paymentsuccessful/', views.paymentsuccessful, name='payment_successful'),
    path('cancel/', views.cancel, name='cancel'),
    path('cancelsubcription/', views.cancel_subscription, name='cancel_subscription')
    

]