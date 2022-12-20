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
    3개월 간격
    분기마다 매너평가 재설정 최근 거래가 신뢰도를 나타냄
    주기를 설정가능하고 매일하면 베스트지만 굳이?
    3분기 전에는 가중치가 1정도임 그래서 일단 지금 1분기는 0.4 가중치로 주고 1분기당 리셋느낌
    다른거 계산하면서 계산해두면 괜찮지 않나? 1주일마다 계산하는거 0.4 해서 모델에 저장하고 숫자 저장하면 계산만해서 가능할 것 같은데 나중에 생각하자
    서버에서 어떻게 돌아갈지 모르니까 일단 그냥 계산하자 나중에 하고싶은거 하고
    리뷰에서시작? 유저에서 시작? for문써서하니까
    여기서 각유저 1분기마다 계산하고
    나중에 csv사용하면 저장된 분기평균 계산하고 지금 분기 계산하고 @평균저장
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
