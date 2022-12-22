# django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404

from .serializers import ReviewCreateSerializer, ReviewListSerializer
from user.serializers import UserSerializer
from goods.models import Goods
from user.models import User
from .models import Review
from django.db.models import Q
import datetime
from datetime import timedelta

class ReviewAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        """
        판매자 정보에 들어갔을때 후기모음
        """
        user_id=request.query_params.get('user_id','')
        reviews=Review.objects.filter(receiver_id=user_id)
        serializer=ReviewListSerializer(reviews, many=True)
        bad_review_count=0
        soso_review_count=0
        good_review_count=0
        excellent_review_count=0
        for review in reviews:
            if review.score==-20:
                bad_review_count +=1
            elif review.score==0:
                soso_review_count +=1
            elif review.score==3:
                good_review_count +=1
            elif review.score==5:
                excellent_review_count +=1
        data = {
            "bad_review_count":bad_review_count,
            "soso_review_count":soso_review_count,
            "good_review_count":good_review_count,
            "excellent_review_count":excellent_review_count,
            "results":serializer.data
        }
        if len(reviews) > 0:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """
        리뷰를 남기면서 상대방의 매너를 평가하는 기능
        """
        goods_id=request.query_params.get('goods_id','')
        goods_obj=Goods.objects.get(id=goods_id)
        review_exist=Review.objects.filter(goods_id=goods_id, author_id=request.user.id).exists()
        serializer = ReviewCreateSerializer(data=request.data, context={'request':request})
        score=(request.data.get('score'))
        if review_exist==True:
            """
            리뷰 1회 제한
            """
            return Response({"message":"이미 평가를 했어요"}, status=status.HTTP_409_CONFLICT)
        else:
            if serializer.is_valid() and request.user.id==goods_obj.seller_id:
                """
                author 셀러일때 review의 receiver 저장
                """
                buyer=get_object_or_404(User, id=goods_obj.buyer_id)
                serializer.save(author = request.user, receiver=buyer, goods = goods_obj)
                buyer.rating_score = buyer.rating_score + int(score)*0.4
                buyer.save()
                print(serializer.data)
                if score != '-20':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    try:
                        receiver_review_score = Review.objects.filter(receiver_id=goods_obj.buyer_id).order_by('-created_at').values()[1]
                        if receiver_review_score['score'] == -20:
                            time_now=datetime.datetime.now()
                            react_at=str(time_now+timedelta(weeks=3))
                            buyer.is_active = 0
                            buyer.react_at = react_at[:10]
                            buyer.save()
                            return Response({"message":"연속적인 비매너로 정지"}, status=status.HTTP_200_OK)
                    except:
                        return Response({"message":"연속적인 비매너는 아니네요"}, status=status.HTTP_200_OK)

            elif serializer.is_valid() and request.user.id==goods_obj.buyer_id:

                """
                author 바이어일때 receiver 저장
                """
                seller=get_object_or_404(User, id=goods_obj.seller_id)
                serializer.save(author = request.user, receiver=seller, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
                seller.rating_score = seller.rating_score + int(score)*0.4
                seller.save()
                print(serializer.data)
                if score != '-20':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    try:
                        receiver_review_score = Review.objects.filter(receiver_id=goods_obj.seller_id).order_by('-created_at').values()[1]
                        if receiver_review_score['score'] == -20:
                            time_now=datetime.datetime.now()
                            react_at=str(time_now+timedelta(weeks=3))
                            seller.is_active = 0
                            seller.react_at = react_at[:10]
                            seller.save()
                            return Response({"message":"연속적인 비매너로 정지"}, status=status.HTTP_200_OK)
                    except:
                        return Response({"message":"연속적인 비매너로 정지"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                
