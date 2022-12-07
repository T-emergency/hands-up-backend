# 
from django.db import models
from user.models import User
from chat.models import TradeChatRoom, AuctionChatRoom



class Goods(models.Model):
    class Meta:
        db_table = 'Goods'
        ordering = ['-created_at'] # 일단 추가해뒀습니다

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_goods')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buy_goods', null=True, blank=True)
    trade_room = models.ForeignKey(TradeChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    auction_room = models.ForeignKey(AuctionChatRoom, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=256)
    content = models.TextField()
    category = models.CharField(max_length=32)
    status = models.BooleanField(default=None, null=True, blank=True)
    predict_price = models.IntegerField()
    start_price = models.IntegerField()
    high_price = models.IntegerField(default=0)
    start_date = models.DateField()
    start_time = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    like = models.ManyToManyField(User, related_name='like_goods', blank=True, null=True)


from django.core.validators import validate_image_file_extension
class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods/',validators=[validate_image_file_extension])

    # 사진 유효성 검사 추가해야함
    # 데이터 이상하게 try

class BidPrice():
    class Meta:
        db_table = 'BidPrice'
        ordering = ['-created_at'] # 일단 추가해뒀습니다

    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    price = models.IntegerField()


