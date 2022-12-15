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
    """
    리뷰를 남기면서 상대방의 매너를 평가하는 기능
    """
    # TODO post하면 바로 점수반영


    def post(self, request, goods_id):
        """
        판매글에서 대화창에 들어왔을때 로컬스토리지, 쿼리파라미터로 받음
        """
        goods_obj=Goods.objects.get(id=goods_id)
        review_exist=Review.objects.filter(goods_id=goods_id, author_id=request.user.id).exists()
        serializer = ReviewCreateSerializer(data=request.data)
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
                buyer.rating_score = buyer.rating_score + int(score)
                buyer.save()
                serializer.save(author = request.user, receiver=buyer, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
                if score != '-20':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    try:
                        receiver_review_score = Review.objects.filter(receiver_id=goods_obj.buyer_id).order_by('-created_at').values()[1]
                        if receiver_review_score['score'] == -20:
                            time_now=datetime.datetime.now()
                            active_at=str(time_now+timedelta(weeks=3))
                            buyer.is_active = 0
                            buyer.react_at = active_at[:10]
                            buyer.save()
                            return Response({"message":"연속적인 비매너로 정지"}, status=status.HTTP_200_OK)
                        return Response({"message":"비매너 사용자입니다"}, status=status.HTTP_200_OK)
                    except:
                        return Response({"message":"연속적인 비매너는 아니네요"}, status=status.HTTP_200_OK)

            elif serializer.is_valid() and request.user.id==goods_obj.buyer_id:
                """
                author 바이어일때 receiver 저장
                """
                seller=get_object_or_404(User, id=goods_obj.seller_id)
                seller.rating_score = seller.rating_score + int(score)
                seller.save()
                serializer.save(author = request.user, receiver=seller, goods = goods_obj) # 포린키에 저장하는건 id str이 아니라 객체임 그래서 객체가져와서 저장해야한다.
                if score != '-20':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    try:
                        receiver_review_score = Review.objects.filter(receiver_id=goods_obj.seller_id).order_by('-created_at').values()[1]
                        if receiver_review_score['score'] == -20:
                            time_now=datetime.datetime.now()
                            active_at=str(time_now+timedelta(weeks=3))
                            seller.is_active = 0
                            seller.react_at = active_at[:10]
                            seller.save()
                            return Response({"message":"연속적인 비매너로 정지"}, status=status.HTTP_200_OK)
                        return Response({"message":"비매너 사용자입니다"}, status=status.HTTP_200_OK)
                    except:
                        return Response({"message":"연속적인 비매너로 정지"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                




class UserInfoAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id):
        
        """
        판매자 정보에 들어갔을때 후기모음
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


