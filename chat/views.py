from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.safestring import mark_safe

from .models import AuctionChatRoom, AuctionMessage
from .serializers import AuctionChatRoomSerializer, AuctionMessageSerializer

class AuctionChatRoomView(APIView):
    def get(self, request):
        chat_room = AuctionChatRoom.objects.all()
        serializer = AuctionChatRoomSerializer(chat_room, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = AuctionChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
class AuctionChatRoomDetailView(APIView):
    def get(self, request, room_id):
        chat_room = AuctionChatRoom.objects.get(id=room_id)
        serializer = AuctionChatRoomSerializer(chat_room)
        return Response(serializer.data)