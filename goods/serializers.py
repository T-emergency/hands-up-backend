from rest_framework import serializers
from .models import Goods,GoodsImage

class GoodImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)
    
    print('goodsimage serializer')
    class Meta:
        model = GoodsImage
        fields =('image',)


class GoodsPostSerializer(serializers.ModelSerializer):
    image = GoodImageSerializer(many=True, read_only = True)

    def get_image(self, obj):
        image = obj.goodsimage_set.all()
        request = self.context['request']
        print('serializer',request)
        return GoodsPostSerializer(instance=image, many = True, context={'request':request})

    class Meta:
        model = Goods
        fields = (
        'seller', 'buyer','auction_room','title','content',
        'category','status','predict_price','start_price','high_price',
        'trade_room','start_date','start_time','created_at','like','image',
        )
        read_only_fields = ("seller",)

    def create(self, validated_data):
        goods = Goods.objects.create(**validated_data)
        print(goods)
        images_data = self.context['request'].FILES
        print(images_data)
        for image_date in images_data.getlist('image'):
            print('image for ')
            GoodsImage.objects.create(goods = goods, image = image_date)
        return goods


