from user.models import User
import datetime

"""
1일 1회 함수
"""

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

"""
비교적 주기가 긴 함수
"""
def anonymous_review():
    """
    1주일 간격
    리뷰 후 일주일 지나고 적용 익명성 보장
    1주일에 한번
    컬럼만들어서 점수 저장해도 된다. 데이터 분산
    """
    users = User.objects.all()
    for user in users:
        user.rating_score = user.rating_score + user.saved_score
        user.saved_score = 0
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
    """

    pass
