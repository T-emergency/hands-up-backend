from user.models import User
from review.models import Review
import datetime
from datetime import timedelta



def prison_break():
    """
    1일 간격
    매일자정 정지 해제되는 회원 active
    """
    users = User.objects.filter(react_at=str(datetime.date.today())[:10])
    for user in users:
        user.is_active = 1
        user.rating_score = 40
        user.save()


def anonymous_review():
    """
    1주일 간격
    리뷰 후 일주일 지나고 적용 익명성 보장
    1주일에 한번
    컬럼만들어서 점수 저장해도 된다. 데이터 분산
    """
    users = User.objects.all()
    for user in users:
        user.rating_score = user.rating_score + user.temp_score
        user.temp_score = 0
        user.save()
        if user.rating_score < 0:
            user.is_active = 0
            user.save()
        else:
            continue


def rating_score_reset():
    """
    3개월 간격 가중치 점수 설정
    """
    # q1부터 가까운 분기
    q1 = 0.4
    q2 = 0.3
    q3 = 0.2
    q4 = 0.1
    update_time = datetime.datetime.now()
    users = User.objects.all()
    for user in users:
        reviews = Review.objects.filter(receiver_id=user.id)
        flag = 0
        for review in reviews:
            score = 0
            if update_time - timedelta(weeks=12) < review.created_at <= update_time:
                score+=review.score * q1
            elif update_time - timedelta(weeks=24) < review.created_at <= update_time - timedelta(weeks=12):
                score+=review.score * q2
            elif update_time - timedelta(weeks=36) < review.created_at <= update_time - timedelta(weeks=24):
                score+=review.score * q3
            elif update_time - timedelta(weeks=48) < review.created_at <= update_time - timedelta(weeks=36):
                score+=review.score * q4
            flag += score
        user.rating_score = 40 + flag
        user.save()
