from user.models import User
import datetime

def cron_user_ban():
    """
    일정주기 유저 정지 함수
    """
    users = User.objects.filter(rating_score__lt=0)
    for i in users:
        i.is_active = 0
        i.save()


def prison_break():
    """
    매일자정 정지 해제되는 회원 active
    """
    users = User.objects.filter(react_at=str(datetime.date.today())[:10])
    for i in users:
        i.is_active = 1
        i.rating_score = 40
        i.save()

