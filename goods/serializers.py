from rest_framework import serializers
from .models import Goods,GoodsImage

class GoodsImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GoodsImage
        fields =['image',]


class GoodsPostSerializer(serializers.ModelSerializer):
    # goodsimage_set = GoodsImageSerializer(many = True, read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        
        image = obj.goodsimage_set.all()
        return GoodsImageSerializer(image, many = True).data

    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ("seller",)

    def create(self, validated_data):
        
        instance = super().create(validated_data)
        image_set = self.context['request'].FILES.getlist('files')
       
        for image_date in image_set:
            GoodsImage.objects.create(goods = instance, image = image_date)
        return instance

