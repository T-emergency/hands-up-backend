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
    # 매너평가 받은 갯수
    # 거래후기 review에서 receiver id 지금 들어온 id인 리뷰 들고옴 작성자 id랑 시간 content 회원정보 이미지도 들고와야함
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




