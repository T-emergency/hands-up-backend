from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import MaxValueValidator, MinValueValidator


from random import randint
import hashlib
import hmac
import base64
import requests
import time
import json
import datetime
from django.utils import timezone

from pathlib import Path
import os
import environ
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
class UserManager(BaseUserManager):
    def create_user(self, phone, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an phone address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            phone=phone,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone=phone,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'User'
    phone = models.CharField(
        verbose_name='phone',
        max_length=15,
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=128,
        unique=True,
    )

    profile_image = models.ImageField(
        upload_to='media', height_field=None, width_field=None, default='default.jpeg', blank=True)
    kakao_id = models.CharField(max_length=100, blank=True)

    rating_score = models.SmallIntegerField(
        default=40,
    )
    temp_score= models.SmallIntegerField(
        default=0,
    )
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    react_at = models.CharField(max_length=12,null=True, blank=True)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin





class AuthSms(models.Model):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'AuthSms'

    def save(self, *args, **kwargs):
        self.auth_number = randint(100000, 1000000)
        super().save(*args, **kwargs)
        self.send_sms()  # 인증번호가 담긴 SMS를 전송

    def send_sms(self):
        id = os.environ.get('NID').strip()
        
        url = f'https://sens.apigw.ntruss.com/sms/v2/services/{id}/messages'
        print(url)
        data = {
            "type": "SMS",
            "contentType" : "COMM",
            "from": os.environ.get('NAVER_FROM_NUMBER').strip(),
            "messages":[{"to":self.phone_number, "subject" : "제목입니다"}],
            "content": "[핸즈업] 본인 확인 인증 번호 [{}]를 입력해주세요.".format(self.auth_number)
        }
        headers = {
            "Content-Type": "application/json",
            "x-ncp-apigw-timestamp" : str(int(time.time() * 1000)),
            "x-ncp-iam-access-key": os.environ.get('NAK').strip(),
            "x-ncp-apigw-signature-v2": self.make_signature(),
        }
        requests.post(url, data=json.dumps(data), headers=headers)


    def	make_signature(self):
        id = os.environ.get('NID').strip()
        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)
        access_key = os.environ.get('NAK').strip()		
        secret_key = os.environ.get('NSK').strip()		
        print(access_key, secret_key, os.environ.get('POSTGRES_DB', ''),os.environ.get('POSTGRES_PORT', ''),os.environ.get('POSTGRES_HOST', ''),os.environ.get('POSTGRES_PASSWORD', ''),os.environ.get('POSTGRES_USER', ''))
        secret_key = bytes(secret_key, 'UTF-8')
        method = "POST"
        URI = f'/sms/v2/services/{id}/messages'
        # URI = "/photos/puppy.jpg?query1=&query2"

        message = method + " " + URI + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    @classmethod
    def check_auth_number(cls, p_num, c_num):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=c_num,
            updated_at__gte=time_limit
        )
        if result:
            return True
        return False