from django.db import models
from user.models import User


class TradeChatRoom(models.Model):
    class Meta:
        db_table = 'TradeChatRoom'
        ordering = ['-created_at']

    created_at = models.DateTimeField(auto_now_add=True)


class TradeMessage(models.Model):
    class Meta:
        db_table = 'TradeMessage'

    author = models.ForeignKey(User, on_delete = models.CASCADE)
    trade_room = models.ForeignKey(TradeChatRoom, on_delete = models.CASCADE)
    content = models.CharField(max_length=500, blank=False)
    is_read = models.BooleanField(default=False)


class AuctionChatRoom(models.Model):
    class Meta:
        db_table = 'AuctionChatRoom'


class AuctionMessage(models.Model):
    class Meta:
        db_table = 'AuctionMessage'
        ordering = ['-created_at']
    
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    auction_room = models.ForeignKey(AuctionChatRoom, on_delete = models.CASCADE)
    content = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)