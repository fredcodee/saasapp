"""Todoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import handler
from django.contrib import admin
from django.urls import path, include
from memberships.views import stripe_webhook, updateaccounts


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('todo.urls')),
    path('membership/', include('memberships.urls')),
    path('stripe_webhook/', stripe_webhook, name = 'stripe_webhook'),
    path('superuser/update/accounts/', updateaccounts, name="update_accounts")
]


handler404 ="todo.views.handle_not_found"
handler500 ="todo.views.handle_server_error"
