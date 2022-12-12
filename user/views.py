from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import CustomTokenObtainPairSerializer, JoinSerializer, UserSerializer,ProfileSerializer
from .models import User
from goods.models import Goods

from goods.serializers import GoodsSerializer

class UserView(APIView):
    def get(self, request):
        users = request.user
        serializer = UserSerializer(users)
        return Response(serializer.data)

    def post(self, request):
        serializer = JoinSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response({'msg': '가입완료'}, status=status.HTTP_201_CREATED)
        # else:
        #     data = dict()
        #     for key in serializer.errors.keys():
        #         data[key] = f"이미 존재하는 {key} 또는 형식에 맞지 않습니다."
        #     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"msg" : f"{serializer.errors}"}, status = status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

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


# User profile
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
        serialize_like = GoodsSerializer(like_goods,many=True)
        print(".........data에 묶기 전")
        user_data = {
            "sell_goods":serialize_sell.data,
            "buy_goods":serialize_buy.data,
            "like_goods":serialize_like.data,
        }
        print('-------data에 묶은 후')

        return Response(user_data)


from .models import AuthSms
class AuthSmsView(APIView):

    def get(self, request):
        try:
            p_num = request.query_params['phone']
            a_num = request.query_params['auth_number']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            result = AuthSms.check_auth_number(p_num=p_num, c_num=a_num)
            return Response({'message':result}, status=status.HTTP_200_OK)


    def post(self, request):
        try:
            p_num = request.data['phone']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            AuthSms.objects.update_or_create(phone_number=p_num)
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    


class UserViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        pass

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '가입완료'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            # return Response({"msg" : f"{serializer.errors}"}, status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, user_id=None):
        """
        회원 정보 수정
        """
        user = request.user

        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(pk=user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '저장완료'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None): # TODO is_delete컬럼 유효기간을 주거나 정보를 가지고 있는 약관 만들어서 가지고 있기

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(pk=request.user.id)
        user.delete()
        return Response(status=status.HTTP_200_OK)


    @action(detail = True, methods=['get'])
    def username_check(self, request, pk=None):
        try:
            username = request.query_params['username']
        except KeyError:
            return Response({'result':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)
        else:
            flag = User.objects.filter(username = username).exists()
            return Response({'result': flag}, status=status.HTTP_200_OK)


    @action(detail = True, methods=['get'], permissions=[])
    def get_info(self, request, pk=None):
        user = request.user
        return Response({'result':'d'}, status=status.HTTP_200_OK)