from rest_framework import serializers
from .models import TradeMessage
from user.serializers import UserSerializer




class TradeMessageSerializer(serializers.ModelSerializer):
    
    author = UserSerializer(read_only = True)
    
    class Meta:
        model = TradeMessage
        fields = '__all__'
        read_only_fields=('author',)