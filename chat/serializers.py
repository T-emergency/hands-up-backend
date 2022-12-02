from rest_framework import serializers
from .models import AuctionChatRoom, AuctionMessage

import locale


locale.setlocale(locale.LC_TIME, 'ko-KR.UTF-8')

class AuctionChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionChatRoom
        fields = '__all__'

class AuctionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionMessage
        fields = '__all__'