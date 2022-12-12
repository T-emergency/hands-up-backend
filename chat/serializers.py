from rest_framework import serializers
from .models import TradeMessage
from user.serializers import UserSerializer




class TradeMessageSerializer(serializers.ModelSerializer):
    
    author = UserSerializer()
    
    class Meta:
        model = TradeMessage
        fields = '__all__'