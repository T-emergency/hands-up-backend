from rest_framework import serializers
from .models import ReportArticle,ReportArticleComment
from user.models import User

class ReportArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportArticle
        fields = '__all__'
        read_only_fields=("author",)

class ReportArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportArticleComment
        fields = '__all__'
        read_only_fields=("author",)