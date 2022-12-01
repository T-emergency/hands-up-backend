from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

# Create your views here.


class ChatView(APIView):

    def get(self, post_id):
        return