# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from back.serializers import UserSerializer, GroupSerializer
import requests
from wechat.settings import wxloginapi
import subprocess


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


def login(data):
    code = data.GET.get("code")
    r = requests.post(wxloginapi, data={
        'appid': 'wxc2856436ce115044',
        'secret': '6107a784b9a3f2750feda6b82fcfbbec',
        'js_code': code,
        'grant_type': 'authorization_code',
    }
    )
    print(r.json())
    return HttpResponse(r.text)
# appid	string		��	С���� appId
# secret	string		��	С���� appSecret
# js_code	string		��	��¼ʱ��ȡ�� code
# grant_type	string		��	��Ȩ���ͣ��˴�ֻ����д authorization_code


def update(request):
    if request.method == 'POST':
        # github�Ĺ��ӱ�������
        data = request.POST
        p = subprocess.Popen('. /Arduino/conf/update', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdout.encoding = 'utf8'
        if p.stdout:
            log.debug('���³ɹ�', p.stdout.read())
        else:
            log.debug('����ʧ��', p.stderr.read())
