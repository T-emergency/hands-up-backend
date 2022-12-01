from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .models import User


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
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            # return Response({"msg" : f"{serializer.errors}"}, status = status.HTTP_400_BAD_REQUEST)

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