# drf
from rest_framework import serializers

# serializer
from user.serializers import UserSerializer

# models
from .models import Goods, GoodsImage



class GoodsImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GoodsImage
        fields =['image',]


class GoodsSerializer(serializers.ModelSerializer):

    seller = UserSerializer(read_only = True)
    buyer = UserSerializer(read_only = True)
    # is_like = serializers.SerializerMethodField()
    # seller = serializers.SerializerMethodField()
    # auction_room = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    # buyer = serializers.SerializerMethodField()

    def get_images(self, obj):
        if self.context["action"] == 'list':
            try:
                return GoodsImageSerializer(obj.goodsimage_set.all()[0]).data
            except IndexError:
                return None
        else:
            return GoodsImageSerializer(obj.goodsimage_set.all(), many = True).data


    def get_is_like(self, obj):
        user = self.context['request'].user
        flag = user in obj.like.all()
        return flag
    
    def get_seller(self,obj):
        return obj.seller.username
        
    def get_buyer(self,obj):
        try:
            username = self.buyer.username
        except:
            return None
        return username


    def create(self, validated_data):
        instance = super().create(validated_data)
        image_set = self.context['request'].FILES.getlist('images')
        image_list = [GoodsImage(goods = instance, image = image) for image in image_set]
        GoodsImage.objects.bulk_create(image_list)
        return instance


    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ['like', 'status']
        
    
    # class Meta:
    #     model = Goods
    #     fields = '__all__'
    #     read_only_fields = ('seller','buyer','trade_room','status','high_price','auction_room')