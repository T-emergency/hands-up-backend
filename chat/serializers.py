from rest_framework import serializers
from .models import AuctionMessage, TradeChatRoom, TradeMessage
from user.serializers import UserSerializer




class TradeMessageSerializer(serializers.ModelSerializer):
    
    author = UserSerializer(read_only = True)
    class Meta:
        model = TradeMessage
        fields = ['content', 'is_read', 'created_at', 'author']

class AuctionMessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        time = obj.created_at
        am_pm = time.strftime('%p')
        now_time = time.strftime('%I:%M')

        if am_pm == 'AM':
          now_time = f"오전 {now_time}"
        else:
          now_time = f"오후 {now_time}"
        return now_time
    class Meta:
        model = AuctionMessage
        fields = '__all__'