# drf
from rest_framework import serializers

# serializer
from user.serializers import UserSerializer

# models
from .models import Goods, GoodsImage
from rest_framework.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from datetime import datetime


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


class TradeInfoSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    buyer = UserSerializer()
    wait_cnt = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_wait_cnt(self, obj):
        msg = obj.trade_room.trademessage_set.all()
        st_idx = len(msg)-10 if len(msg)-10 > 0 else 0
        return len([ 0 for message in msg[st_idx:] if message.author_id != self.context['request'].user.id and message.is_read == False])

    def get_image(self, obj):
        try:
            return obj.goodsimage_set.all()[0].image.url
        except IndexError:
            return None
    def get_last_message(self, obj):
        try:
            # last_message = obj.trade_room.trademessage_set.order_by('-created_at')[0]
            last_message = obj.trade_room.trademessage_set.all()
            last_message = last_message[len(last_message)-1]
            data = {
                'message' : last_message.content,
                'created_at' : last_message.created_at
            }
            return data
        except IndexError:
            data = {
                'message' : '거래를 시작해 주세요!',
                'created_at' : datetime.now()
            }
            return data

    class Meta:
        model = Goods
        fields = ['id', 'seller', 'buyer', 'image', 'wait_cnt', 'title', 'high_price', 'last_message']