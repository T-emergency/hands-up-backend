from rest_framework import serializers
from .models import Review
from user.models import User

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields=('goods','author','receiver')


class ReviewListSerializer(serializers.ModelSerializer):
    # TODO 판매상품 4개
    author = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    created_at= serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def get_receiver(self, obj):
        return obj.receiver.username
    
    def get_created_at(self,obj):
        return str(obj.created_at)[:19]
    class Meta:
        model = Review
        fields = '__all__'




