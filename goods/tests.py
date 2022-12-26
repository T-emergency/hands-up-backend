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
    image=Image.new("RGBA",size,color)
    image.save(temp_file,'png')
    return temp_file

class GoodsCreateTest(APITestCase):
    """
    판매상품 등록
    """
    @classmethod
    def setUpTestData(cls):
        # Goods.objects.create(
        #     id=1,
        #     # "title":"test",
        #     # "content":"test",
        #     # "category":"기타",
        #     # "status":"0",
        #     predict_price=15000,
        #     start_price=10000,
        #     # "high_price":"0",
        #     start_date='2022-12-25',
        #     start_time='1159',
        #     seller_id=1,
        # )
        # User.objects.create(
        #     id=1
        # )
        # cls.user_data={'phone':'010','username':'test','password':'!1testtest'}
        # cls.user=User.objects.create_user('010','test','!1testtest')
        cls.goods_data={
            "title":"test",
            "content":"test",
            "category":"기타",
            # "status":"0",
            "predict_price":"15000",
            "start_price":"10000",
            # "high_price":"0",
            "start_date":"2022-12-25",
            "start_time":"11:59"
            # "seller_id":0
            }

    def setUp(self):
        self.user_data={'phone':'010','username':'test','password':'!1testtest'}
        self.user=User.objects.create_user('010','test','!1testtest')
        # self.access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']

    def test_create_goods(self):
        access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']
        response = self.client.post(
            path=reverse("goods_view"),
            HTTP_AUTHORIZATION="Bearer"+" "+access_token,
            data=self.goods_data,
        )
        print(response.data)
        print(access_token)
        self.assertEqual(response.status_code,201)

    def test_create_goods_image(self):
        # 임시 이미지파일 생성
        temp_file=tempfile.NamedTemporaryFile()
        temp_file.name="image.png"
        image_file=get_temporary_image(temp_file)
        image_file.seek(0)
        self.goods_data["image"]=image_file
        access_token=self.client.post(reverse('token_obtain'), self.user_data).data['access']
        # 전송
        response=self.client.post(
            path=reverse("goods_view"),
            data=encode_multipart(data=self.goods_data,boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION="Bearer"+" "+access_token,
            )
        # print(response.data)
        # print(self.access_token)
        self.assertEqual(response.status_code,201)
        
# class GoodsCreateTest(APITestCase):
#     """
#     판매상품 등록
#     """
#     def setUp(self):
#         self.user_data={'phone':'010','username':'test','password':'!1testtest'}
#         self.goods_data={
#             "title":"test",
#             "content":"test",
#             "category":"기타",
#             "status":"0",
#             "predict_price":"15000",
#             "start_price":"10000",
#             "high_price":"0",
#             "start_date":"2022-12-25",
#             "start_time":"11:59",
#         }
#         self.user=User.objects.create_user('010','test','!1testtest')
#         self.access_token=self.client.post(reverse('token_obtain'), self.data).data['access']
#     def test_create
            #     seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell_goods")
    # buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buy_goods", null=True, blank=True)
    # trade_room = models.ForeignKey(TradeChatRoom, on_delete=models.CASCADE, null=True, blank=True)

    # title = models.CharField(max_length=256)
    # content = models.TextField()
    # category = models.CharField(max_length=32)
    # status = models.BooleanField(null=True, blank =True)
    # predict_price = models.IntegerField()
    # start_price = models.IntegerField()
    # high_price = models.IntegerField(default=0 ,null=True, blank=True)
    # start_date = models.DateField()
    # start_time = models.CharField(max_length=5)
    # created_at = models.DateTimeField(auto_now_add=True)
    # like = models.ManyToManyField(User, related_name='like_goods', blank=True, null=True)