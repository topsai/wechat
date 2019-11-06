# Create your views here.
import requests
import subprocess
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from back.models import Article
from rest_framework import viewsets
from back.serializers import UserSerializer, GroupSerializer, ArticleSerializer
from wechat.settings import wxloginapi
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)


def login(request):
    if request.method == 'POST':
        code = request.GET.get("code")
        r = requests.post(wxloginapi, data={
            'appid': 'wxc2856436ce115044',
            'secret': '6107a784b9a3f2750feda6b82fcfbbec',
            'js_code': code,
            'grant_type': 'authorization_code',
        }
                          )
        print(r.json())
        return HttpResponse(r.text)
    if request.method == 'GET':
        print('get')
        str = '<h1>hello world</h1>'
        return HttpResponse(str)
    else:
        print("ee")
