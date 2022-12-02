from rest_framework import serializers

from .models import Goods, GoodsImage, BidPrice

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        models = Goods
        fields = '__all__'
        read_only_fields = ('seller','buyer','trade_room','status','high_price')
        

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        models = GoodsImage
        field = '__all__'

class BidPriceSerializer(serializers.ModelSerializer):
    class Meta:
        models = BidPrice
        fields = '__all__'
        read_only_fields = ('buyer',)