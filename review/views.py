# django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .serializers import ReviewCreateSerializer
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
        goods_obj=Goods.objects.get(id=goods_id)
        serializer = ReviewCreateSerializer(data=request.data)
        review_exist=Review.objects.filter(goods_id=goods_id, user_id=request.user.id).exists()
        if review_exist==False:
            if serializer.is_valid():
                serializer.save(user = request.user, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
                score=serializer.data.get('manner_score')
                if request.user.id==goods_obj.seller_id:
                    """
                    후기를 작성한 사람이 셀러라면 바이어를 평가한다.
                    """
                    buyer_id=goods_obj.buyer_id
                    user = get_object_or_404(User, id=buyer_id)
                    user.rating_score = user.rating_score + score
                    user.save()
                    if score == -20:
                        """
                        평가받은 바이어가 최악의 점수를 받았다면 바이어의 최근 거래점수를 확인하고 연속적으로 비매너점수를 받았다면 정지를 시킨다.
                        """
                        buyer_goods_id = Goods.objects.filter(buyer_id=buyer_id) | Goods.objects.filter(seller_id=buyer_id)
                        buyer_goods_id_value=buyer_goods_id.order_by('-created_at').values()[:2] # score 없으면 다른거 들고오게는 나중에
                        first_buyer_goods_id = buyer_goods_id_value[1]['id']
                        second_buyer_goods_id = buyer_goods_id_value[0]['id']
                        first_reviews = Review.objects.filter(goods_id=first_buyer_goods_id).exclude(user_id=buyer_id)
                        second_reviews = Review.objects.filter(goods_id=second_buyer_goods_id).exclude(user_id=buyer_id)
                        try:
                            if first_reviews.values()[0]['manner_score']+second_reviews.values()[0]['manner_score'] == -40:
                                ban_user = User.objects.get(id = buyer_id)
                                ban_user.is_active = 0
                                ban_user.save()
                                return Response(serializer.data, status=status.HTTP_200_OK)
                        except:
                            return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        pass
                elif request.user.id==goods_obj.buyer_id:
                    """
                    후기를 작성한 사람이 바이어라면 셀러를 평가한다.
                    """
                    seller_id=goods_obj.seller_id
                    user = get_object_or_404(User, id=seller_id)
                    user.rating_score = user.rating_score + score
                    user.save()
                    if score == -20:
                        """
                        평가받은 셀러가 최악의 점수를 받았다면 셀러의 최근 거래점수를 확인하고 연속적으로 비매너점수를 받았다면 정지를 시킨다.
                        """
                        seller_goods_id = Goods.objects.filter(seller_id=seller_id) | Goods.objects.filter(buyer_id=seller_id)
                        seller_goods_id_value=seller_goods_id.order_by('-created_at').values()[:2]
                        first_seller_goods_id = seller_goods_id_value[1]['id']
                        second_seller_goods_id = seller_goods_id_value[0]['id']
                        first_reviews = Review.objects.filter(goods_id=first_seller_goods_id).exclude(user_id=seller_id)
                        second_reviews = Review.objects.filter(goods_id=second_seller_goods_id).exclude(user_id=seller_id)
                        try:
                            if first_reviews.values()[0]['manner_score']+second_reviews.values()[0]['manner_score'] == -40:
                                ban_user = User.objects.get(id = seller_id)
                                ban_user.is_active = 0
                                ban_user.save()
                                return Response(serializer.data, status=status.HTTP_200_OK)
                        except:
                            return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        pass
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("이미 평가를 했어요", status=status.HTTP_400_BAD_REQUEST)




class ReviewListAPIView(APIView):
    def get(self, request, user_id):
        """
        판매자 정보에 들어갔을때 후기모음
        """
        goods = Goods.objects.filter(seller_id=user_id)
