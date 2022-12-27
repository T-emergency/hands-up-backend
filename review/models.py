# model
from django.db import models
from user.models import User
from goods.models import Goods
from django.core.validators import MaxValueValidator, MinValueValidator



class Review(models.Model):
    class Meta:
        db_table = 'Review'
        ordering = ['-created_at']

    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='review_author')
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name='review_receiver')
    goods = models.ForeignKey(Goods, on_delete = models.CASCADE)
    content = models.CharField(max_length=50)
    score = models.SmallIntegerField(
            validators=[
            MaxValueValidator(5),
            MinValueValidator(-20)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

