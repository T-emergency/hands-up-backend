from django.contrib import admin
from .models import TradeChatRoom, TradeMessage, AuctionChatRoom, AuctionMessage

# Register your models here.
admin.site.register(TradeChatRoom)
admin.site.register(TradeMessage)
admin.site.register(AuctionChatRoom)
admin.site.register(AuctionMessage)