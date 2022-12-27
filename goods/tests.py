from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User
from goods.models import Goods
from goods.models import GoodsImage

# 이미지 업로드
from django.test.client import MULTIPART_CONTENT,encode_multipart,BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size=(1,1)
    color=(255,0,0,0)
    images=Image.new("RGBA",size,color)
    images.save(temp_file,'png')
    return temp_file

class GoodsCreateTest(APITestCase):
    """
    goods 등록
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods_data={
            "title":"test",
            "content":"test",
            "category":"기타",
            "predict_price":"15000",
            "start_price":"10000",
            "start_date":"2022-12-25",
            "start_time":"11:59"
            }

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_create_goods(self):
        response = self.client.post(
            path=reverse("goods_view"),
            data=self.goods_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code,201)

    def test_create_goods_with_image(self):
        # 임시 이미지파일 생성
        temp_file=tempfile.NamedTemporaryFile() # 파이썬 임시파일 만듬
        temp_file.name="image.png"
        image_file=get_temporary_image(temp_file)
        image_file.seek(0)
        self.goods_data["images"]=image_file
        # 전송
        response=self.client.post(
            path=reverse("goods_view"),
            data=encode_multipart(data=self.goods_data,boundary=BOUNDARY), #굿즈 데이터에 이미지 추가
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )
        self.assertEqual(response.status_code,201)


class GoodsLikeTest(APITestCase):
    """
    goods like
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1
            )

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_goods_like(self):
        response = self.client.get(
            '/goods/like/1/',
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code,200)



class GoodsListTest(APITestCase):
    """
    goods list
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1
            )
        cls.goods=Goods.objects.create(
            id=2,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1
            )

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_goods_list(self):
        response = self.client.get(
            '/goods/',
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        # print(response.data)
        self.assertEqual(response.status_code,200)



class GoodsDetailTest(APITestCase):
    """
    goods detail
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1
            )

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_goods_detail(self):
        response = self.client.get(
            '/goods/1/',
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        # print(response)
        # print(response.data)
        self.assertEqual(response.status_code,200)


class GoodsRecommendTest(APITestCase):
    """
    goods recommend
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1
            )

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_goods_recommend(self):
        response = self.client.get(
            path=reverse('goods_recommend'),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code,200)


class UserGoodsViewTest(APITestCase):
    """
    user goods view 
    """
    @classmethod
    def setUpTestData(cls):
        cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods=Goods.objects.create(
            id=1,
            predict_price=1,
            start_price=1,
            start_date='2022-12-29',
            seller_id=1
            )

    def setUp(self):
        self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_goods_recommend(self):
        response = self.client.get(
            '/goods/user/1/',
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code,200)