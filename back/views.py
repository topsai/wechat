#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@Time :    2019/11/8 15:32
@Author:  "范斯特罗夫斯基" John
@File: WXBizDataCrypt.py
@Software: PyCharm
"""
# Create your views here.
import requests
import subprocess
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import Group
from .models import User
from back.models import Article
from rest_framework import viewsets
from back.serializers import UserSerializer, GroupSerializer, ArticleSerializer
from wechat.settings import wxloginapi
from rest_framework.permissions import IsAuthenticated
import json
from .WXBizDataCrypt import WXBizDataCrypt

appId = 'wxb11c8642b5007e82'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticated,)


import base64
from Crypto.Cipher import AES


def create_session(openid, session_key):
    # openid + session_key 生成session
    session = openid + session_key
    # 编码： 字符串 -> 二进制 -> base64编码
    b64_name = base64.b64encode(session.encode()).decode()
    print('加密session', b64_name)
    return b64_name


def decode_session(session, session_key):
    # 解码：base64编码 -> 二进制 -> 字符串
    a = base64.b64decode(session).decode()
    b = a.strip(session_key)
    print('解码session, 获取 openid', b)
    return b


# 加密方法
def encrypt_oracle():
    # 秘钥
    key = '123456'
    # 待加密文本
    text = 'abc123def456'
    # 初始化加密器
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    # 先进行aes加密
    encrypt_aes = aes.encrypt(str.encode(text))
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    print(encrypted_text)


# 解密方法
def decrypt_oralce():
    # 秘钥
    key = '123456'
    # 密文
    text = 'qR/TQk4INsWeXdMSbCDDdA=='
    # 初始化加密器
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8')  # 执行解密密并转码返回str
    print(decrypted_text)


def login(request):
    if request.method == 'POST':

        print('session', request.headers.get('Session'))
        print(request.session)
        code = ""
        user = ""
        userinfo = ""
        ret_data = {
            'state': 'ok'
        }
        try:
            # 登陆 注册
            code = json.loads(request.body).get('code')
        except:
            pass
        try:
            # 获取 unionid
            userinfo = json.loads(request.body).get('userinfo')
        except:
            pass
        if code:
            # 更新微信session_key
            print('code', code)
            # 调用微信接口通过appid， secret， js_code 获取session_key 及 openid
            r = requests.post(wxloginapi, data={
                'appid': appId,
                'secret': '41035b5dc2c09eb18123ddd0c90d3be3',
                'js_code': code,
                'grant_type': 'authorization_code',
            }
                              )
            print('json', r.json())
            session_key = r.json().get('session_key')
            openid = r.json().get('openid')
            # 通过 openid 查看用户是否存在
            try:
                user = User.objects.filter(openid=openid).first()
                # user = User.objects.first(openid=openid)
            except:
                print('用户不存在')
            # 用户已经存在
            if user:
                # 用户存在更新session key
                print('用户存在更新session key')
                user.session_key = session_key
            else:
                # 用户第一次登陆，根据微信openid创建用户
                print('用户第一次登陆，根据微信openid创建用户')
                user = User.objects.create_user(username=openid, password='', session_key=session_key, openid=openid)
            # 创建并保存session
            session = create_session(openid, session_key)
            user.session = session
            user.save()
            # 生成 session 并返回给小程序
            ret_data['session'] = session
        elif userinfo:
            request_session = request.headers.get('Session')
            user = User.objects.filter(session=request_session).first()
            # 解码 unionid
            print('unionid')
            print(userinfo)
            print(type(userinfo))
            rawData = json.loads(userinfo.get('rawData'))
            nickName = rawData.get('nickName')
            print(userinfo.get('rawData'), type(userinfo.get('rawData')))
            print('nickName', rawData.get('nickName'))
            print('signature', userinfo.get('signature'))
            print('encryptedData', userinfo.get('encryptedData'))
            print('iv', userinfo.get('iv'))
            print('cloudID', userinfo.get('cloudID'))
            # decode_session(user.session, user.session_key)
            # User.objects.first(openid=openid)
            # session_key =
            print(user.session_key)
            pc = WXBizDataCrypt(appId, user.session_key)
            decrypt_data = pc.decrypt(userinfo.get('encryptedData'), userinfo.get('iv'))
            print(decrypt_data)
            unionId = decrypt_data.get('unionId')
            user.unionid = unionId
            user.nickname = nickName
            user.save()
            print('unionId', unionId)

        return HttpResponse(json.dumps(ret_data))
    if request.method == 'GET':
        print('get')
        str = '<h1>hello world</h1>'
        return HttpResponse(str)
    else:
        print("ee")
