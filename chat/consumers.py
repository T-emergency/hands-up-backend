# utils
import json
from datetime import datetime

# channels
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import get_user_model

# models
from goods.models import Goods, BidPrice
from user.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['goods_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # TODO user permission
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        is_money = text_data_json.get('is_money', '')
        goods_id = text_data_json.get('goods_id', '')
        user_id = text_data_json.get('goods_id', '')


        # TODO return exception 찾아보기
        if '' in [user_id, goods_id, is_money]:
          return '?'

        user = await self.get_user_obj(user_id)

        if is_money == True:
          goods = await self.get_goods_obj(goods_id)

          if goods == False: # 방어 코드 (상품 x)
            return False

          if goods.seller_id == user_id: # 방어코드 (주최자가 경매입찰)
            return False

          try: # 방어 코드
            money = int(text_data_json['message'])
          except ValueError:
            return False
          
          await self.set_high_price(goods, user_id, money)

          response = {
            'sender': user.id,
            'sender_name': user.username,
            'goods_id': goods_id,
            'high_price' : goods.high_price
          }

        else:
          message = text_data_json['message']


          now = datetime.now()
          am_pm = now.strftime('%p')      
          now_time = now.strftime('%I:%M')
          now_date = now.strftime('%Y년 %m월 %d일 %A')

          if am_pm == 'AM':
            now_time = f"오전 {now_time}"
          else:
            now_time = f"오후 {now_time}"

          response = {
            'message': message,
            'sender': user.id,
            'sender_name': user.username,
            'goods_id': goods_id,
            'date': now_date,
            'time': now_time,
          }

          # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'response': json.dumps(response)

            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=event['response'])
    

    @database_sync_to_async
    def set_high_price(self, goods:object, user_id, money):

        if goods.high_price > money: # 방어코드
          return False

        goods.high_price = money
        goods.buyer_id = user_id
        goods.save()
          

    @database_sync_to_async
    def get_user_obj(self, user_id):

      try:
        obj = User.objects.get(pk = user_id)
      except User.DoesNotExist:
        return False
      return obj

    @database_sync_to_async
    def get_goods_obj(self, goods_id):

      try:
        obj = Goods.objects.get(pk = goods_id)
      except Goods.DoesNotExist:
        return False
      return obj