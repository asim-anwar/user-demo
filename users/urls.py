from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('register', UserRegView, basename='user-register')
router.register('login', UserLoginView, basename='user-login')


urlpatterns = [
    path('', include(router.urls)),
    # path('login', UserLoginView.as_view(), name='user-login')
]