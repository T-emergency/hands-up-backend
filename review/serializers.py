from rest_framework import serializers
from .models import Review
from user.models import User
from django.utils.html import escape


class ReviewCreateSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        review=super().create(validated_data)
        review.content = escape(self.context['request'].data['content'])
        review.save()
        return review

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields=('goods','author','receiver')

class ReviewListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    created_at= serializers.SerializerMethodField()

    def get_author(self, obj):
        print(obj.author.username)
        return obj.author.username

    def get_receiver(self, obj):
        return obj.receiver.username
    
    def get_created_at(self,obj):
        return str(obj.created_at)[:19]

    class Meta:
        model = Review
        fields = '__all__'




