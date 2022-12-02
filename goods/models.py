from django.db import models
from user.models import User
from chat.models import TradeChatRoom, AuctionChatRoom



class Goods(models.Model):
    class Meta:
        db_table = 'Goods'
        ordering = ['-created_at'] # 일단 추가해뒀습니다

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_goods')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_goods', null=True)
    trade_room = models.ForeignKey(TradeChatRoom, on_delete=models.CASCADE, blank=True, null=True)
    auction_room = models.ForeignKey(AuctionChatRoom, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=256)
    content = models.TextField()
    category = models.CharField(max_length=32, blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    predict_price = models.IntegerField(blank=True, null=True)
    start_price = models.IntegerField(blank=True, null=True)
    high_price = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    start_time = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    like = models.ManyToManyField(User, related_name='like_goods', blank=True, null=True)


# class Goods(models.Model):
#     class Meta:
#         db_table = 'Goods'
#         ordering = ['-created_at'] # 일단 추가해뒀습니다

#     seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_goods')
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_goods', null=True)
#     trade_room = models.ForeignKey(TradeChatRoom, on_delete=models.CASCADE)
#     auction_room = models.ForeignKey(AuctionChatRoom, on_delete=models.CASCADE)

#     title = models.CharField(max_length=256)
#     content = models.TextField()
#     category = models.CharField(max_length=32)
#     status = models.BooleanField(blank=True)
#     predict_price = models.IntegerField()
#     start_price = models.IntegerField()
#     high_price = models.IntegerField(blank=True)
#     start_date = models.DateField()
#     start_time = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     like = models.ManyToManyField(User, related_name='like_goods', blank=True)



class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods/')



class BidPrice():
    class Meta:
        db_table = 'BidPrice'
        ordering = ['-created_at'] # 일단 추가해뒀습니다

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    price = models.IntegerField()


