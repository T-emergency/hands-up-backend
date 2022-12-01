from rest_framework import serializers
from .models import FreeArticle 


class FreeArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeArticle
        fields = "__all__"