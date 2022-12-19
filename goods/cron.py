from .models import Goods
from chat.models import TradeChatRoom
from datetime import date, datetime, timedelta
from django.db.models import Q
# import pytz

def auction_start_and_end():
    today = date.today()
    yesterday = ((datetime.now() - timedelta(days=1)))
    end_day = (datetime.now() - timedelta(minutes=20))
    start_time = datetime.now().time().strftime('%H:%M')
    end_time = (datetime.now() - timedelta(minutes=20)).time().strftime('%H:%M')
    
    start_q = Q(start_date=today, start_time__lte=start_time,status=None)
    start_errors_q = Q(start_date__lte=yesterday, status=None)
    auction_start_list = Goods.objects.filter(start_q | start_errors_q)

    if auction_start_list.exists():
        for goods in auction_start_list:
            goods.status = True
            goods.save()
            
    end_q = Q(start_date=end_day.date(), start_time__lte=end_time, status=True)    
    end_errors_q = Q(start_date__lte=yesterday,status=True)
    
    if yesterday.date() == end_day.date():
         end_errors_q = Q(start_date__lt=yesterday,status=True)
         
    auction_end_list = Goods.objects.filter(end_q | end_errors_q)
    
    if auction_end_list.exists():
        for goods in auction_end_list:
            goods.status = False
            goods.save()

    goods_list = Goods.objects.filter(status=False, trade_room=None,buyer__isnull=False)
    
    if goods_list.exists():
        for goods in goods_list:
            room = TradeChatRoom.objects.create()
            goods.trade_room = room
            goods.save()
            
    print(f'date: {today}T{start_time}')
    print("auction_start: ",auction_start_list)        
    print("auction_end: ",auction_end_list)        
    print("create_trade_room: ",goods_list)