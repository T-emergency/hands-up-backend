from rest_framework import serializers

from .models import Goods, GoodsImage, BidPrice



class GoodsImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GoodsImage
        fields =['image',]



class GoodsSerializer(serializers.ModelSerializer):
    seller = serializers.SerializerMethodField()
    auction_room = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()


    def get_images(self, obj):
        image = obj.goodsimage_set.all()
        return GoodsImageSerializer(image, many = True).data
    

    def get_seller(self,obj):
        return obj.seller.username
        
    
    def get_auction_room(self, obj):
        return obj.auction_room.id
        
    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ('seller','buyer','trade_room','status','high_price','auction_room')


    def create(self, validated_data):
        
        instance = super().create(validated_data)
        image_set = self.context['request'].FILES.getlist('files')
       
        for image_date in image_set:
            GoodsImage.objects.create(goods = instance, image = image_date)
        return instance

     
     
class BidPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidPrice
        fields = '__all__'
        read_only_fields = ('buyer',)
