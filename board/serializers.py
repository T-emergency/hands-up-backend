from rest_framework import serializers
from .models import ReportArticle,ReportArticleComment,FreeArticle
from user.models import User

class ReportArticleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        return obj.author.username
        
    class Meta:
        model = ReportArticle
        fields = '__all__'
        read_only_fields=("author",)




class ReportArticleCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        return obj.author.username
    class Meta:
        model = ReportArticleComment
        fields = '__all__'
        read_only_fields=("author",)




class FreeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"




class FreeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = ('title', 'content', 'author', 'image',)
        read_only_fields = ('author','image',)
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




class FreeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"

