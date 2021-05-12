from django.db import models

# Create your models here.


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

    class Meta:
        db_table = 'user'

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'birth_day': str(self.birth_day),
            'avatar': self.avatar,
            'location': self.location,
        }


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

    def to_dict(self):
        return {
            'id': self.id,
            'dating_sex': self.dating_sex,
            'dating_location': self.dating_location,
            'min_dating_age': self.min_dating_age,
            'max_dating_age': self.max_dating_age,
            'min_distance': self.min_distance,
            'max_distance': self.max_distance,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }