from rest_framework import serializers
from .models import Review

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields=('user','goods','author','receiver')


class ReviewListSerializer(serializers.ModelSerializer):
    # TODO 판매상품 4개
    # 매너평가 받은 갯수
    # 거래후기 review에서 receiver id 지금 들어온 id인 리뷰 들고옴 작성자 id랑 시간 content 회원정보 이미지도 들고와야함

    class Meta:
        model = Review
        fields = '__all__'
        # 이후 굿즈랑 id 들고와서 사용해야함
        # 클릭해서 들어가면 보여주는건 



