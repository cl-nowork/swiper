from django.db import models
from django.db.models import Q

from commons import status


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
        return cls.objects.filter(uid=uid, sid=sid, stype__in=['like', 'superlike']).exists()

    @classmethod
    def swipe(cls, uid, sid, stype):
        '''执行滑动'''
        if stype not in ['like', 'dislike', 'superlike']:
            raise ValueError('stype 参数错误')
        if cls.objects.filter(uid=uid, sid=sid).exists():
            raise status.SwipeRepeatError(msg='重复滑动')
        else:
            return cls.objects.create(uid=uid, sid=sid, stype=stype)

    @classmethod
    def who_liked_me(cls, uid):
        '''都有谁喜欢我'''
        return cls.objects.filter(sid=uid, stype__in=['like', 'superlike']).values_list('uid', flat=True)


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
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def friend_ids(cls, uid):
        '''查询uid下的所有好友ID'''
        condition = Q(uid1=uid) | Q(uid2=uid)
        friends = Friend.objects.filter(condition)
        uid_list = []
        for friend in friends:
            friend_id = friend.uid2 if friend.uid1 == uid else friend.uid1
            uid_list.append(friend_id)
        return uid_list

    @classmethod
    def break_off(cls, uid, sid):
        '''删除好友关系'''
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()
