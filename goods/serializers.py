# drf
from rest_framework import serializers

# serializer
from user.serializers import UserSerializer

# models
from .models import Goods, GoodsImage
from rest_framework.exceptions import ValidationError
from django.core.files.images import get_image_dimensions



class GoodsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsImage
        fields =['image',]


class GoodsSerializer(serializers.ModelSerializer):

    seller = UserSerializer(read_only = True)
    buyer = UserSerializer(read_only = True)
    is_like = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()

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

    def get_participants_count(self, obj):
        if self.context["action"] == 'list':
            return obj.auctionparticipant_set.count()
        else:
            return 0
            
    def validate(self, data):
        # 바이트 기준
        file_size= 5242880 # 5MB
        required_width = 5000
        required_height = 5000
        image_set = self.context['request'].FILES.getlist('images')
        for i in image_set:
            width, height = get_image_dimensions(i)
            if i.size > file_size:
                raise ValidationError("사진용량 초과")
            elif width > required_width or height > required_height:
                print(width,height)
                raise ValidationError("사진크기 초과")
        return data

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



class GoodsListSerializer(serializers.ModelSerializer):

    seller = serializers.StringRelatedField()
    buyer = serializers.StringRelatedField()
    is_like = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()

    def get_image(self, obj):
        try:
            return GoodsImageSerializer(obj.goodsimage_set.all()[0]).data
            # return obj.goodsimage_set.all()[0].image.url
        except IndexError:
            return None

    def get_is_like(self, obj):
        user = self.context['request'].user
        flag = user in obj.like.all()
        return flag

    def get_participants_count(self, obj):
        return obj.auctionparticipant_set.count()


    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ['like', 'status']