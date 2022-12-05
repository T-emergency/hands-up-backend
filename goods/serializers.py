from rest_framework import serializers
from .models import Goods,GoodsImage

class GoodImageSerializer(serializers.ModelSerializer):
    print('이미지 시리얼 라이즈')
    image = serializers.ImageField(use_url=True)
    
    print('goodsimage serializer')
    class Meta:
        model = GoodsImage
        fields =['image',]


class GoodsPostSerializer(serializers.ModelSerializer):
    image = GoodImageSerializer(many = True, read_only=True)

    def get_image(self, obj):
        image = obj.image.all()
        # request = self.context['request']
        # print('serializer',request)
        return GoodsPostSerializer(instance=image, many = True, context = self.context).data
        # context={'request':request}
    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ("seller",)

    def create(self, validated_data):
        goods = Goods.objects.create(**validated_data)
        print(goods.id)
        images_data = self.context['request'].FILES
        # print('serializer 이미지 데이터',images_data)
        for image_date in images_data.getlist('image'):
            print('image for')
            GoodsImage.objects.create(goods = goods, image = image_date)
        return goods


