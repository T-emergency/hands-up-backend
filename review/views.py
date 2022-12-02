# django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .serializers import ReviewCreateSerializer
from goods.models import Goods
from user.models import User


class ReviewAPIView(APIView):
    """
    리뷰를 남기면서 상대방의 매너를 평가하는 기능
    """

    # TODO 우선 구매자만
    # 테이블 나눠서 바이어 셀러 or 신고자 피신고자 하면 좋을 거 같긴한데 안나누려면 이름 포스트 저장해두고
    # 바이어가 유저로 바뀌고 굿즈에서 구매자 판매자 가져와서 유저가
    # 굿즈에 들어가서 
    # goods에 구매자 판매자 둘 다 있다. goods_id와
    # 거래한거만 후기 가능 거래한거 굿즈 확인가능 채팅방을 가져온다 get

    def post(self, request, goods_id):
        """
        판매글에서 대화창에 들어왔을때 로컬스토리지, 쿼리파라미터로 받음
        Review.object.get(user=request.user, goods=goods_id)
        """
        print(request.data)
        print(request.user)
        print(goods_id)
        goods_obj=Goods.objects.get(id=goods_id)
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def post(self, request, trade_room_id):
    #     """
    #     판매글이 아닌 다른곳(개인 페이지)에서 채팅방을 들어왔을때
    #     정리:로컬스토리지에서 받아서 쿼리파라미터로 받아옴
    #     path로 받아오면 url에 있는거 파라미터로 바로 사용 - path는 댓글처럼 post있는곳에서 연관된거 할때
    #     쿼리로 받아로면 url에 있는거 get해서 사용
    #     """
    #     category_name=request.GET.get('category','')

    #     goods = Goods.objects.get(trade_room_id)
    #     goods_id = goods.trade_room
    #     # Review.object.get(user=request.user, goods=goods_id)
    #     serializer = ReviewCreateSerializer(data=request.data)
    #     print(request.data)
    #     if serializer.is_valid():
    #         serializer.save(user = request.user, goods=goods_id)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def post(self, request, study_id, student_id):
#     student = get_object_or_404(Student, id = student_id)
#     if student.post.user.id == request.user.id:
#         student.is_accept = True
#         student.save()
#         return Response(status=status.HTTP_200_OK)
#     else:
#         return Response("권한이 없습니다.")

# def post(self, request): # 생성
#     print(request.user)
#     serializer= ArticleCreateSerializer(data=request.data) #user post 비직렬화
#     if serializer.is_valid():
#         serializer.save(user=request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReviewAPIView(APIView):
