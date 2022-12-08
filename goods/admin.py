from django.contrib import admin
from .models import Goods, BidPrice, GoodsImage
# Register your models here.
admin.site.register(Goods)
admin.site.register(GoodsImage)
admin.site.register(BidPrice)
