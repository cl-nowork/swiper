from django.db import models


class Swiped(models.Model):
    '''滑动记录'''
    STYPE = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的UID')
    sid = models.IntegerField(verbose_name='被滑动者的UID')
    stype = models.CharField(max_length=10, choices=STYPE, verbose_name='滑动的类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        db_table = 'swiped'

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        return cls.objects.filter(uid=uid, sid=sid,
                                  stype__in=['like', 'superlike']).exists()


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    class Meta:
        db_table = 'friend'

    @classmethod
    def make_friend(cls, uid, sid):
        '''创建好友关系接口'''
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        cls.objects.create(uid1=uid1, uid2=uid2)
