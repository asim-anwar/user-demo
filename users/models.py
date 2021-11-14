from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

