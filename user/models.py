from django.db import models
from vip.models import Vip


class User(models.Model):
    SEX = (('male', '男性'), ('female', '女性'))
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('广州', '广州'),
        ('深圳', '深圳'),
        ('浙江', '浙江'),
    )
    phonenum = models.CharField(max_length=16, verbose_name='手机号')
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_day = models.DateField(default='1990-1-1', verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')
    location = models.CharField(max_length=20, choices=LOCATION, verbose_name='常居地')
    ext_uid = models.CharField(max_length=16, unique=True, null=True, blank=True, verbose_name='第三登录的唯一标识')

    vip_id = models.IntegerField(default=1, verbose_name='用户对应的vip')
    vip_expired = models.DateTimeField(default='2000-1-1', verbose_name='会员过期时间')

    class Meta:
        db_table = 'user'

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def to_dict_after_exclude(self):
        return self.to_dict('vip_id', 'ext_uid', 'vip_expired')


class Profile(models.Model):
    '''交友资料'''
    dating_sex = models.CharField(max_length=8, choices=User.SEX, verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=20, choices=User.LOCATION, verbose_name='目标城市')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=30, verbose_name='最大查找范围')

    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='是否只让匹配的人看到')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放')

    class Meta:
        db_table = 'profile'
