from user.models import User


def cron_user_ban():
    """
    일정주기 유저 정지 함수
    """
    users = User.objects.filter(rating_score__lt=0)
    for i in users:
        i.is_active = 0
        i.save()

    