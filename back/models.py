from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=256)
    img = models.ImageField(upload_to='img')
    content = models.CharField(max_length=256)
    introduction = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now=True)
    money = models.IntegerField()
    inventory = models.IntegerField()

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("car")


# SuperUser : admin   Password:admin


class OrderInfo(models.Model):
    # 订单金额
    quota = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quota

    class Meta:
        pass
        # verbose_name = '订单详情'
        # verbose_name_plural = '订单详情'


from django.contrib.auth.models import AbstractUser


# 扩展用户模型
class User(AbstractUser):
    # 微信官方数据
    nickname = models.CharField(max_length=32)
    session_key = models.CharField(max_length=32)
    openid = models.CharField(max_length=32)
    unionid = models.CharField(max_length=32)
    # 自定义session
    session = models.CharField(max_length=256)
