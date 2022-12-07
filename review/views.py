# django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .serializers import ReviewCreateSerializer, ReviewListSerializer
from goods.models import Goods
from user.models import User
from .models import Review
from django.db.models import Q


class ReviewAPIView(APIView):
    """
    리뷰를 남기면서 상대방의 매너를 평가하는 기능
    """
    # TODO post하면 바로 점수반영
    # 중복금지
    # 1주일에 한번씩 평가 낮은사람 정지, 메일
    # 평가 낮지만 위험은 경고메일
    # 리뷰평가를 한번에 계산해서 넘겨준다 = 당근
    # 한번 남기면 남기지 못하게
    # 한사람이 한번만 평가가능
    # 조건걸어서 판매자면 구매자 점수내리는 로직
    # 테이블 나눠서 바이어 셀러 or 신고자 피신고자 하면 좋을 거 같긴한데 안나누려면 이름 포스트 저장해두고
    # goods에 구매자 판매자 둘 다 있다. goods_id와
    # 거래한거만 후기 가능 거래한거 굿즈 확인가능 채팅방을 가져온다 get
    # 다 만들었는데 간과한점 최근글 두개라서 1234글중에 12평가하면 정지안당한다.
    # 업데이트 만들까? 다른정보 업데이트할수도

    def post(self, request, goods_id):
        """
        판매글에서 대화창에 들어왔을때 로컬스토리지, 쿼리파라미터로 받음
        Review.object.get(user=request.user, goods=goods_id)
        """
        # TODO 같은사람에게 리뷰 불가능하게 한다. 나중에 좋은평가 할 수 없다? or 사기를 당했다 그럴땐 문의해야지
        # 리시버한테 남기면 그 goods에 자동으로 못남김 함께 해결될 듯
        # 판매자와 구매자가 바뀌면 또 평가 해야하지 않을까?
        # request data 활용해서 쿼리줄이기 시리얼라이저 통과하면 사용하는 값이라서 괜찮을듯
        # 작성자, 리시버 한번이라도 평가했다면 평가 불가능하게도 가능
        goods_obj=Goods.objects.get(id=goods_id)
        review_exist=Review.objects.filter(goods_id=goods_id, author_id=request.user.id).exists()
        serializer = ReviewCreateSerializer(data=request.data)
        score=int(request.data.get('score'))
        if review_exist==True:
            """
            리뷰 1회 제한
            """
            return Response("이미 평가를 했어요", status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid() and request.user.id==goods_obj.seller_id:
                """
                author 셀러일때 review의 receiver 저장
                """
                buyer=get_object_or_404(User, id=goods_obj.buyer_id)
                buyer.rating_score = buyer.rating_score + int(score)
                buyer.save()
                serializer.save(author = request.user, receiver=buyer, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
                if score != -20:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    try:
                        receiver_review_score = Review.objects.filter(receiver_id=goods_obj.buyer_id).order_by('-created_at').values()[1]
                        if receiver_review_score['score'] == -20:
                            buyer.is_active = 0
                            buyer.save()
                            return Response("연속적인 비매너로 정지", status=status.HTTP_200_OK)
                    except:
                        return Response("연속적인 비매너는 아니네요", status=status.HTTP_200_OK)

            elif serializer.is_valid() and request.user.id==goods_obj.buyer_id:
                """
                author 바이어일때 receiver 저장
                """
                seller=get_object_or_404(User, id=goods_obj.seller_id)
                seller.rating_score = seller.rating_score + int(score)
                seller.save()
                serializer.save(author = request.user, receiver=seller, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
                if score != -20:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    try:
                        receiver_review_score = Review.objects.filter(receiver_id=goods_obj.seller_id).order_by('-created_at').values()[1]
                        if receiver_review_score['score'] == -20:
                            seller.is_active = 0
                            seller.save()
                            return Response("연속적인 비매너로 정지", status=status.HTTP_200_OK)
                    except:
                        return Response("연속적인 비매너는 아니네요", status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                




class ReviewListAPIView(APIView):
    def get(self, request, user_id):
        """
        판매자 정보에 들어갔을때 후기모음
        """
        review_list = Review.objects.filter(receiver_id=user_id)
        review_list_order_by = review_list.order_by('-created_at')
        serializer=ReviewListSerializer(review_list_order_by, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
