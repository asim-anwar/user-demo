from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=None)
    mobile_number = models.CharField(max_length=13)
    nid = models.BigIntegerField(default=None)
    address = models.CharField(max_length=300, null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

