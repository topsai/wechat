# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from back.models import Article
from rest_framework import viewsets
from back.serializers import UserSerializer, GroupSerializer, ArticleSerializer
import requests
from wechat.settings import wxloginapi
import subprocess
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)


def login(r):
    print(r)
    str = u'<h1>hello world</h1>'
    return HttpResponse(str)
    # if request.method == 'POST':
    #     code = request.GET.get("code")
    #     r = requests.post(wxloginapi, data={
    #         'appid': 'wxc2856436ce115044',
    #         'secret': '6107a784b9a3f2750feda6b82fcfbbec',
    #         'js_code': code,
    #         'grant_type': 'authorization_code',
    #     }
    #                       )
    #     print(r.json())
    #     return HttpResponse(r.text)
    # if request.method == 'GET':
    #     print('get')
    #     str = '<h1>hello world</h1>'
    #     return HttpResponse(str)
    # else:
    #     print("ee")


# appid	string		是	小程序 appId
# secret	string		是	小程序 appSecret
# js_code	string		是	登录时获取的 code
# grant_type	string		是	授权类型，此处只需填写 authorization_code


def update(request):
    if request.method == 'POST':
        # github的钩子被触发了
        data = request.POST
        p = subprocess.Popen('. /Arduino/conf/update', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdout.encoding = 'utf8'
        if p.stdout:
            # log.debug('更新成功', p.stdout.read())
            pass
        else:
            pass
            # log.debug('更新失败', p.stderr.read())
