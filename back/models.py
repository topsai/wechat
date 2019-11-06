from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # �ּ�
    min_price = models.SmallIntegerField()
    # ԭ��
    max_price = models.SmallIntegerField()
    pic = models.CharField(max_length=256)

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("car")


# SuperUser : admin   Password:admin


class OrderInfo(models.Model):
    # �������
    quota = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.quota

    class Meta:
        pass
        # verbose_name = '��������'
        # verbose_name_plural = '��������'
