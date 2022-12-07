from rest_framework import serializers

from .models import Goods, GoodsImage, BidPrice

class GoodsSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    auction_room = serializers.SerializerMethodField()
    
    def get_seller(self,obj):
        return obj.seller.username
        
    
    def get_auction_room(self, obj):
        return obj.auction_room.id
    
    # def create(self, validated_data):
    #     validated_data['auction_room'] = self.context['auction_room']

    #     instance = super().create(validated_data)
    #     return instance

    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ('seller','buyer','trade_room','status','high_price','auction_room')
        

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        field = '__all__'

class BidPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidPrice
        fields = '__all__'
        read_only_fields = ('buyer',)