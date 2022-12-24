from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.db import models
from .models import User

class UserRegistrationTest(APITestCase):
    """
    회원가입
    """
    def test_registration(self):
        url=reverse("user_view")
        user_data={
            "username":"test",
            "phone":"010",
            "password":"!1testtest"
        }
        response = self.client.post(url, user_data)
        print(response)
        self.assertEqual(response.status_code,201)


class LoginUserTest(APITestCase):
    """
    로그인 테스트코드
    """
    def setUp(self):
        self.data={'phone':'010','username':'test','password':'!1testtest'}
        self.user=User.objects.create_user('010','test','!1testtest')

    def test_login(self):
        response=self.client.post(reverse('token_obtain'),self.data)
        self.assertEqual(response.status_code,200)

    def test_get_user_data(self):
        access_token=self.client.post(reverse('token_obtain'), self.data).data['access']
        response=self.client.get(
            path=reverse('user_view'),
            HTTP_AUTHORIZATION=f"Bearer{access_token}"
        )
        self.assertEqual(response.status_code,200)
