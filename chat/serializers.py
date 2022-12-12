from rest_framework import serializers
from .models import TradeMessage




class TradeMessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    
    def get_author(self, obj):
        return obj.author.username
    
    class Meta:
        model = TradeMessage
        fields = '__all__'