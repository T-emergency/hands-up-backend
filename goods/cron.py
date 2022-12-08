from .models import Goods
from chat.models import TradeChatRoom
from datetime import date, datetime, timedelta
# import pytz

def test_one_minute():
    print("use crontab")
    
    
def auction_start_and_end():
    today = date.today()
    start_time = datetime.now().time().strftime('%H:%M')
    print("start_time: ",start_time)
    auction_start_list = Goods.objects.filter(start_date=today, start_time=start_time)
    print(auction_start_list)
    if auction_start_list.exists():
        for goods in auction_start_list:
            goods.status = True
            goods.save()
    
    end_time = (datetime.now() - timedelta(minutes=20)).time().strftime('%H:%M')
    print("end_time: ",end_time)
    auction_end_list = Goods.objects.filter(status=True, start_date=today, start_time=end_time)
    print(auction_end_list)
    if auction_end_list.exists():
        for goods in auction_end_list:
            goods.status = False
            goods.save()


def get_goods_status():
    print('reading auction..')
    goods_list = Goods.objects.filter(status=False, trade_room=None,buyer__isnull=False)
    if goods_list.exists():
        for goods in goods_list:
            room = TradeChatRoom.objects.create()
            goods.trade_room = room
            goods.save()
    print(goods_list)