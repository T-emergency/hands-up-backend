from rest_framework import serializers
from .models import TradeChatRoom, TradeMessage
from user.serializers import UserSerializer




class TradeMessageSerializer(serializers.ModelSerializer):
    
    author = UserSerializer(read_only = True)
    class Meta:
        model = TradeMessage
        fields = ['content', 'is_read', 'created_at', 'author']