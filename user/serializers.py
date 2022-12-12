# drf
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
    class Meta:
        model = User
        fields = '__all__'#['username', 'password','profile_image']
        extra_kwargs = {
            'password': {'write_only': True},
            "username": {"error_messages": {"required": "Give yourself a username"}}
        }

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# class userProfileReivewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = "__all__"

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
