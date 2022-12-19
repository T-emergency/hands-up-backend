from django.db import models
# models
from user.models import User
from chat.models import TradeChatRoom

# validators
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError

# 이게 에러가 뜨네요
def validate_minimum_size(width=None, height=None):
    def validator(image):
        error = False
        if width is not None and image.width < width:
            error = True
        if height is not None and image.height < height:
            error = True
        if error:
            raise ValidationError(
                [f'Size should be at least {width} x {height} pixels.']
            )
    return validator


class Goods(models.Model):
    class Meta:
        db_table = "Goods"
        ordering = ["-created_at"]  # 일단 추가해뒀습니다

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell_goods")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buy_goods", null=True, blank=True)
    trade_room = models.ForeignKey(TradeChatRoom, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=256)
    content = models.TextField()
    category = models.CharField(max_length=32)
    status = models.BooleanField(null=True, blank =True)
    predict_price = models.IntegerField()
    start_price = models.IntegerField()
    high_price = models.IntegerField(default=0 ,null=True, blank=True)
    start_date = models.DateField()
    start_time = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='like_goods', blank=True, null=True)


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods/',validators=[validate_image_file_extension, validate_minimum_size(width=1, height=1)])


    class Meta:
        db_table = "GoodsImage"