from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
from goods.models import Goods
from review.models import Review

class ReviewCreateTest(APITestCase):
    """
    리뷰작성
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.review_data={'score':'5','content':'test','goods':'1','author':'1','receiver':'2'}
        cls.user1=User.objects.create_user('010','test','!1testtest')
        cls.user2=User.objects.create_user('011','test2','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1,
            buyer_id=2
            )

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_review_post(self):
        response = self.client.post(
            '/review/?goods_id=1',
            data=self.review_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code,200)


class ReviewListTest(APITestCase):
    """
    유저 받은리뷰 보기
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user1=User.objects.create_user('010','test','!1testtest')
        cls.user2=User.objects.create_user('011','test2','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1,
            buyer_id=2
            )
        cls.reviews=Review.objects.create(
            author_id=2,
            receiver_id=1,
            goods_id=1,
            content='test',
            score=5
        )
    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_review_list(self):
        response = self.client.get(
            '/review/?user_id=1',
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        print(response.data)
        self.assertEqual(response.status_code,200)