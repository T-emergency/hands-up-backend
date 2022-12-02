from rest_framework import serializers
from .models import Review

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields=('user','goods')


