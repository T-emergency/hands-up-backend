from django.db import models
from user.models import User


class TradeChatRoom(models.Model):
    class Meta:
        db_table = 'TradeChatRoom'
        ordering = ['-created_at']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TradeMessage(models.Model):
    class Meta:
        db_table = 'TradeMessage'

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    trade_room = models.ForeignKey(TradeChatRoom, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class AuctionParticipant(models.Model):
    class Meta:
        db_table = 'AuctionParticipant'

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    goods = models.ForeignKey("goods.Goods", on_delete = models.CASCADE)