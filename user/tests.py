from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import status
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .models import User

