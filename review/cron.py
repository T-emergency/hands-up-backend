from user.models import User

# TODO 세번연속 안좋은 평가는 바로 정지
# 정지시킬때 확인? 아니면 평가 받았을때 마다 확인?
# 일단 연속적이면 바로 정지 - views 에서 등록 할때마다 확인
# -인거 보고 그사람들만 모으고 그사람들의 2회평가까지 보고 다 음수면 정지 - cron
def cron_user_ban():
    """
    일정주기 유저 정지 함수
    """
    users = User.objects.filter(rating_score__lt=0)
    for i in users:
        i.is_active = 0
        i.save()

