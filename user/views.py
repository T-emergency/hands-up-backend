from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import CustomTokenObtainPairSerializer, UserSerializer,ProfileSerializer,UserProfileSerializer,ReviewListSerializer
from .models import User
from goods.models import Goods
from review.models import Review

# from goods.serializers import GoodsPostSerializer
from goods.serializers import GoodsSerializer

class UserView(APIView):
    def get(self, request):
        users = request.user
        serializer = UserSerializer(users)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '가입완료'}, status=status.HTTP_201_CREATED)
        else:
            data = dict()
            for key in serializer.errors.keys():
                data[key] = f"이미 존재하는 {key} 또는 형식에 맞지 않습니다."
            # return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg" : f"{serializer.errors}"}, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = User.objects.get(pk=request.user.id)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '저장완료'}, status=status.HTTP_200_OK)
        else:
            data = dict()
            for key in serializer.errors.keys():
                data[key] = f"이미 존재하는 {key} 또는 형식에 맞지 않습니다."
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.delete()
        return Response(status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# User profile goods list
class UserProfileView(APIView):
    def get(self, request, user_id):
        #판매내역
        sell_goods = Goods.objects.filter(seller_id = user_id)
        serialize_sell = GoodsSerializer(sell_goods, many=True)
        #구매내역
        buy_goods = Goods.objects.filter(buyer_id = user_id)
        serialize_buy = GoodsSerializer(buy_goods,many=True)
        #관심목록
        like_goods = Goods.objects.filter(like = user_id)

        serialize_like = GoodsPostSerializer(like_goods,many=True)

        #user정보
        user = User.objects.get(id = user_id)
        serialize_user = UserProfileSerializer(user)
        


        serialize_like = GoodsSerializer(like_goods,many=True)
        print(".........data에 묶기 전")

        user_data = {
            "sell_goods":serialize_sell.data,
            "buy_goods":serialize_buy.data,
            "like_goods":serialize_like.data,
            "user_data":serialize_user.data,
        }


        return Response(user_data)


#user profile profile

# class UserProfileReviewView(APIView):
#     def get(self, request, user_id):
#         print('get함수 실행')
#         # user image와 name 가져오기
#         user = User.objects.get(id=user_id)
#         print(user)
#         user_evaluation = user.user_review_set.all()
#         print(user_evaluation)
#         serialize_review = userProfileReivewSerializer(user_evaluation, many=True)
#         serialize_user = UserProfileSerializer(user)

#         context = {
#             "review_user":serialize_review.data,
#             "user_data":serialize_user.data
#         }

#         return Response(context)

class UserProfileReviewView(APIView):
    def get(self, request, user_id):
            
            """
            내 정보에 들어갔을때 후기모음
            """
            review_list=Review.objects.filter(receiver_id=user_id)
            review_list_order_by = review_list.order_by('-created_at')
            serializer=ReviewListSerializer(review_list_order_by, many=True)

            bad_review_count = review_list.filter(score=-20).count()
            soso_review_count = review_list.filter(score=0).count()
            good_review_count = review_list.filter(score=3).count()
            excellent_review_count = review_list.filter(score=5).count()

            receiver=User.objects.get(id=user_id)
            receiver_serializer=UserSerializer(receiver)

            image=[]
            for review in review_list_order_by:
                author=UserSerializer(review.author).data['profile_image']
                image.append(author)

            data = {
                "bad_review_count":bad_review_count,
                "soso_review_count":soso_review_count,
                "good_review_count":good_review_count,
                "excellent_review_count":excellent_review_count,
                "results":serializer.data,
                "receiver":receiver_serializer.data,
                "review_image":image
            }

            return Response(data, status=status.HTTP_200_OK)
            