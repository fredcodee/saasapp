from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=False, default='')

    def __str__(self):
        return self.email