# model
from django.db import models
from user.models import User
from goods.models import Goods



class Review(models.Model):
    class Meta:
        db_table = 'Review'
        ordering = ['-created_at']

    
    buyer = models.ForeignKey(User, on_delete = models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete = models.CASCADE)
    content = models.CharField(max_length=500, blank=False)
    manner_score = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
