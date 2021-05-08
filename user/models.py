from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性')
    )
    LOCATION = (
        ('北京','北京'),
        ('上海','上海'),
        ('广州','广州'),
        ('深圳','深圳'),
    )
    phonenum = models.CharField(max_length=16, verbose_name='手机号')
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_day = models.DateField(default='1990-1-1', verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=20, choices=LOCATION, verbose_name='常居地')

    class Meta:
        db_table = 'user'