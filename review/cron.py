from user.models import User
import datetime
from datetime import timedelta

def cron_user_ban():
    """
    일정주기 유저 정지 함수
    """
    users = User.objects.filter(rating_score__lt=0)
    for i in users:
        i.is_active = 0
        i.save()


def react_user():
    """
    매일새벽 오늘 정지 해제되는 회원 active 기능
    """
    users = User.objects.filter(react_at=datetime.date.today()[:10])
    for i in users:
        i.is_active = 1
        i.save()

