# utils
import json
from datetime import datetime

# channels
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import get_user_model

# models
from goods.models import Goods
from user.models import User
from chat.models import AuctionParticipant, TradeMessage

from chat.serializers import TradeMessageSerializer
from goods.serializers import GoodsSerializer
# 싹다 추가
# 에러 준다. 그룹에서 특정 유저에게


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['goods_id']
        self.room_group_name = 'auction_%s' % self.room_name
        

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


        if self.scope.get('user').is_authenticated:

          goods_id = self.scope['url_route']['kwargs']['goods_id']
          user = self.scope.get('user')
          self.alert_room_name = 'alert_%s' % user.id

          # 해당 로그인 유저 그룹 생성 추가
          await self.channel_layer.group_add(
            self.alert_room_name,
            self.channel_name
          )

          is_first, participants_count = await self.enter_or_out_auction(user.id , goods_id, is_enter = True)

          if is_first:
            response = {
              'response_type' : "enter",
              'sender': user.id,
              'sender_name': user.username,
              'participants_count' : participants_count
            }
            await self.channel_layer.group_send(
              self.room_group_name,
              {
                  'type': 'chat_message',
                  'response': json.dumps(response)

              }
            )

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        if self.scope.get('user').is_authenticated:

          await self.channel_layer.group_discard(
            self.alert_room_name,
            self.channel_name
          )

          user = self.scope.get('user')
          goods_id = self.scope['url_route']['kwargs']['goods_id']
          _, participants_count = await self.enter_or_out_auction(user.id , goods_id, is_enter = False)

          response = {
            'response_type' : "out",
            'participants_count' : participants_count
          }

          await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'response': json.dumps(response)

            }
          )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        is_money = text_data_json.get('is_money', '')
        goods_id = text_data_json.get('goods_id', '')
        user_id = text_data_json.get('user_id', '')


        # 로그인한 유저에게만 alert메시지 전송
        if '' in [user_id, goods_id, is_money]:
          return await self.channel_layer.group_send(
              self.alert_room_name,
              {
                  'type': 'chat_message',
                  'response': json.dumps({'response_type' : 'alert', 'message' : '로그인 하셨나용'})

              }
            )

        user = await self.get_user_obj(user_id)

        if is_money == True:
          goods = await self.get_goods_obj(goods_id)

          if goods == False: # 방어 코드 (상품 x)
            return False

          if goods.seller_id == user_id :#or goods.status != True: # 방어코드 (주최자가 경매입찰, 상품 상태)
            response = {
            'response_type' : "alert",
            'message' : '주최자는 입찰을 못 합니다.'
            }
            await self.channel_layer.group_send(
              self.alert_room_name,
              {
                  'type': 'chat_message',
                  'response': json.dumps(response)

              }
            )
            return 

          try: # 방어 코드
            money = int(text_data_json['message'])
          except ValueError:
            return False
          
          is_high = await self.set_high_price(goods, user_id, money)
          if not is_high:
            response = {
            'response_type' : "alert",
            'message' : '현재 입찰가보다 낮거나 종료된 경매입니다.'
            }
            return await self.channel_layer.group_send(
              self.alert_room_name,
              {
                  'type': 'chat_message',
                  'response': json.dumps(response)

              }
            )

          response = {
            'response_type' : "bid",
            'sender': user.id,
            'sender_name': user.username,
            'sender_image': user.profile_image.url,
            'goods_id': goods_id,
            'high_price' : goods.high_price
          }

        else:
          message = text_data_json['message']

          response = {
            'response_type' : "message",
            'message': message,
            'sender': user.id,
            'sender_name': user.username,
            'goods_id': goods_id,
            'time': await self.get_time(),
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


    async def get_time(self):
      
        now = datetime.now()
        am_pm = now.strftime('%p')      
        now_time = now.strftime('%I:%M')

        if am_pm == 'AM':
          now_time = f"오전 {now_time}"
        else:
          now_time = f"오후 {now_time}"

        return now_time
          

    @database_sync_to_async
    def set_high_price(self, goods:object, user_id, money):

        if goods.high_price > money or goods.status != True: # 방어코드
          return False

        goods.high_price = money
        goods.buyer_id = user_id
        goods.save()
        return True
          

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

    @database_sync_to_async
    def enter_or_out_auction(self, user_id:int, goods_id:int, is_enter:bool):
      """
      경매방에 출/입 에 따라 참여자를 제거/생성|가져오기 를 끝내고 참여자를 반환합니다.

      return bool, int
      """

      # get_or_create()를 사용해서 participants에서 사용 불가
      participants = AuctionParticipant.objects.filter(goods_id = goods_id)
      # create 된다면 True 반환
      participant, is_first = AuctionParticipant.objects.get_or_create(goods_id = goods_id,user_id = user_id)


      if is_enter:
        return is_first, participants.count()
      else:
        participant.delete()
        return is_first, participants.count()


class ChatConsumerDirect(AsyncWebsocketConsumer):

    async def connect(self):

      user = self.scope.get('user')
      goods_id = self.scope['url_route']['kwargs']['goods_id']
      goods = await self.get_goods_obj(goods_id)
      buyer = goods.buyer_id
      seller = goods.seller_id

      if user.is_authenticated and (user.id == buyer or user.id == seller):
        self.room_name = self.scope['url_route']['kwargs']['goods_id']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
          
        await self.accept()
      else:
        # await self.disconnect()
        return False


    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        

        # if self.scope.get('user').is_authenticated:

        #   await self.channel_layer.group_discard(
        #     self.alert_room_name,
        #     self.channel_name
        #   )


    # Receive message from WebSocket
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        goods_id = text_data_json.get('goods_id', '')
        user_id = text_data_json.get('user_id', '')
        
        user = await self.get_user_obj(user_id)
        goods = await self.get_goods_obj(goods_id)
        trade_room_id = goods.trade_room_id
        # trade_room_id = goods["trade_room"]

        message = text_data_json['message']
        
        
        response = {
          'response_type' : "message",
          'message': message,
          'sender': user.id,
          'sender_image': user.profile_image.url,
          'sender_name': user.username,
          'goods_id': goods_id,
          'time': await self.get_time(),
        }        

        if response["sender"] == goods.buyer_id or response["sender"] == goods.seller_id:

          await self.create_trade_message_obj(user_id, message, trade_room_id)

        else:
          # await self.disconnect()
          return False
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


    async def get_time(self):

        now = datetime.now()
        am_pm = now.strftime('%p')      
        now_time = now.strftime('%I:%M')

        if am_pm == 'AM':
          now_time = f"오전 {now_time}"
        else:
          now_time = f"오후 {now_time}"

        return now_time
          

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
    

    @database_sync_to_async
    def get_trade_message_obj(self, trade_room_id):

      obj = TradeMessage.objects.filter(trade_room_id = trade_room_id)
      serializer = TradeMessageSerializer(obj,many=True)

      return serializer.data
    
    
    @database_sync_to_async
    def create_trade_message_obj(self, user_id, message, trade_room_id):

      obj = TradeMessage.objects.create(author_id=user_id, content=message, trade_room_id = trade_room_id)

      return obj
    


class AlramConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if self.scope.get('user').is_authenticated:

          user = self.scope.get('user')
          self.alram_name = 'alram_%s' % user.id

          # 해당 로그인 유저 그룹 생성 추가
          await self.channel_layer.group_add(
            self.alram_name,
            self.channel_name
          )

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.alram_name,
            self.channel_name
        )

    async def chat_message(self, event):
        await self.send(text_data=event['response'])