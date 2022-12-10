from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from channels.layers import get_channel_layer
from .consumers import ChatConsumer
from asgiref.sync import async_to_sync
from rest_framework.response import Response
import json
# Create your views here.


class ChatView(APIView):

    def get(self, reqeust,goods_id):
        layer = get_channel_layer()
        print(dir(layer), layer)
        async_to_sync(layer.group_send)(f'chat_{goods_id}', {'type': 'chat_message', 'response': json.dumps({'response_type': 'message', 'message': 'hi'})})
        
        return Response('연결 성공')
