from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(UserSubsription)
