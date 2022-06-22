from django.urls import path
from . import views

urlpatterns = [
    path("viewplans/", views.viewPlans, name='view_plans'),
    path('upgradeplan/', views.upgradeplan, name =" upgrade_plan")
,]