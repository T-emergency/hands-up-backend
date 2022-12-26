from django.urls import reverse
from rest_framework.test import APITestCase
from user.models import User

# class ReviewCreateTest(APITestCase):
#     """
#     리뷰작성
#     """
#     def setUp(self):
#         self.user_data={'phone':'010','username':'test','password':'!1testtest'}
#         self.goods_data={
            
#         }
#         self.user=User.objects.create_user('010','test','!1testtest')

#         self.access_token=self.client.post(reverse('token_obtain'), self.data).data['access']

#     def test_registration(self):
#         pass


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