from rest_framework import serializers
from .models import AuctionChatRoom, AuctionMessage, TradeMessage

import locale


# locale.setlocale(locale.LC_TIME, 'ko-KR.UTF-8')

class AuctionChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionChatRoom
        fields = '__all__'

class AuctionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionMessage
        fields = '__all__'
        

class TradeMessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.username
    
    class Meta:
        model = TradeMessage
        fields = '__all__'