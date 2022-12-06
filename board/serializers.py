from rest_framework import serializers
from .models import FreeArticle 


class FreeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"


class FreeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = ('title', 'content', 'author', 'image',)
        extra_kwargs = {'title': {
                        'error_messages': {
                        'required': '제목을 입력해주세요',
                        'blank':'제목을 입력해주세요',}},

                        'content':{
                        'error_messages': {
                        'required':'내용을 입력해주세요.',
                        'blank':'내용을 입력해주세요.',}},
                        }


class FreeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"


class FreeCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"


class FreeCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"

