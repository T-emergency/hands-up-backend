# drf
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import re

# model
from user.models import User
from goods.models import Goods
from review.models import Review

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['user_id'] = user.id
        token['phone'] = user.phone

        return token



class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        return obj.profile_image.url
    class Meta:
        model = User
        # fields = '__all__'#['username', 'password','profile_image']
        extra_kwargs = {
            'password': {'write_only': True},
            "username": {"error_messages": {"required": "Give yourself a username"}}
        }
        exclude = ('last_login', 'phone', 'kakao_id', 'temp_score', 'password')


    def create(self, validated_data):
        user  = super().create(validated_data) # 저장하고
        password = user.password
        user.set_password(password) # 지정하고
        user.save() # 다시 저장?
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"




from rest_framework.exceptions import ValidationError

class JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password','phone']
        extra_kwargs = {
            'password': {'write_only': True},
            "username": {"error_messages": {
                "required": "아이디를 입력해 주세요.",
                "invalid": "이미존재하는 아이디",
                }}
        }


    def create(self, validated_data):

        user  = super().create(validated_data) # 저장하고
        password = user.password
        user.set_password(password) # 지정하고
        user.save() # 다시 저장?
        return user


    def validate_password(self, pw):

        REGEX_PASSWORD = '^(?=.*[a-zA-Z])((?=.*\d)(?=.*\W)).{8,16}$'
        if not re.search(REGEX_PASSWORD, pw):
            raise serializers.ValidationError(detail="비밀번호 8자 이상 16이하 영문, 숫자, 특수문자 하나 이상씩 포함해 주세요.")

        return pw


    # def validate_phone(self, number):
    #     print(number)

    #     REGEX_PHONE = '^01(?=.*[0-9]).{8,9}$'
    #     if not re.search(REGEX_PHONE, number):
    #         raise serializers.ValidationError(detail="'-' 없이 숫자 10자 혹은 11자를 입력해 주세요.")
    #     if User.objects.filter(phone = number).exists():
    #         raise serializers.ValidationError(detail="이미 존재하는 번호에요!")

    #     return number


    # def validate_username(self, username):

    #     REGEX_USERNAME = '^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{1,10}$'

    #     if not re.search(REGEX_USERNAME, username.strip()):
    #         raise serializers.ValidationError(detail="2자리이상 10자리 이하")

    #     if User.objects.filter(username = username).exists():
    #         raise serializers.ValidationError(detail="이미 존재하는 아이디에요!")

    #     return username
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

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