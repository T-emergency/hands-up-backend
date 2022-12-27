from .models import Goods
from chat.models import TradeChatRoom
from datetime import date, datetime, timedelta
from django.db.models import Q

# alram section
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


def auction_start_and_end():

    layer = get_channel_layer()
    today = date.today()
    yesterday = ((datetime.now() - timedelta(days=1)))
    end_day = (datetime.now() - timedelta(minutes=20))
    start_time = datetime.now().time().strftime('%H:%M')
    end_time = (datetime.now() - timedelta(minutes=20)).time().strftime('%H:%M')
    
    start_q = Q(start_date=today, start_time__lte=start_time,status=None)
    start_errors_q = Q(start_date__lte=yesterday, status=None)
    auction_start_list = Goods.objects.filter(start_q | start_errors_q).prefetch_related('like')
    if auction_start_list.exists():

        # TODO 로직 최적화 생각하기
        for goods in auction_start_list:
            data = {
                'response_type' : 'alram',
                'message' : '경매가 시작됐어요',
                'goods_id' : goods.id,
                'goods_title' : goods.title,
            }
            for receiver in goods.like.all():
                # TODO send()로는 안되는지 확인
                async_to_sync(layer.group_send)(f'alram_{receiver.id}', {'type': 'chat_message', 'response': json.dumps(data)})
                # layer.send(channel=f'alram_{receiver.id}', message=json.dumps(data))

            auction_start_list.update(status=True)
    end_q = Q(start_date=end_day.date(), start_time__lte=end_time, status=True)    
    end_errors_q = Q(start_date__lte=yesterday,status=True)
    
    if yesterday.date() == end_day.date():
         end_errors_q = Q(start_date__lt=yesterday,status=True)
         
    auction_end_list = Goods.objects.filter(end_q | end_errors_q).prefetch_related('buyer')
    
    if auction_end_list.exists():
        for goods in auction_end_list:
            data = {
                'response_type' : 'alram',
                'message' : '낙찰 되었습니다!',
                'goods_id' : goods.id,
                'goods_title' : goods.title,
            }
            room = TradeChatRoom.objects.create()
            async_to_sync(layer.group_send)(f'alram_{goods.buyer.id}', {'type': 'chat_message', 'response': json.dumps(data)})
            goods.trade_room = room
            goods.save()
        auction_end_list.update(status=False)