# from django.urls import reverse
# from rest_framework.test import APITestCase
# # from rest_framework.test import status
# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# class UserManager(BaseUserManager):
#     def create_user(self, username, phone, password=None):
#         if not username:
#             raise ValueError('need username')
#             user=self.model(
#                 username=usernmae
#             )

# class ReviewAPIViewTestCase(APITestCase):
#     def setUp(self) -> None:
#         self.data={

#         }
#         self.user=User.objects.create_user('john','johnpassword')
#     def test_review(self):
#         url=reverse("review")
#         review_data = {
#             "id":4,
#             "score":"-20",
#             "content":"별로에요"
#         }
#         response = self.client.post(url,review_data)
#         print(response.data)
#         self.assertEqual(response.status_code,200)
