from collections import OrderedDict

from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

# models
from goods.models import Goods