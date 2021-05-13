import time
import datetime

from django.db import transaction

from user.models import User
from social.models import Swiped, Friend
from swiper import config
from libs.cache import rds
from commons import status
from commons.keys import SUPERLIKED_KEY_FORMAT, REWIND_KEY_FORMAT


def rcmd(user):
    """推荐可滑动的用户"""
    profile = user.profile
    today = datetime.datetime.now()

    min_birth_day = today - datetime.timedelta(profile.max_dating_age * 365)
    max_birth_day = today - datetime.timedelta(profile.min_dating_age * 365)

    # 已经滑过的用户
    sid_list = Swiped.objects.filter(uid=user.id).values_list('sid', flat=True)

    # 从缓存中拿出的用户
    superlike_list = [int(id) for id in rds.zrange(SUPERLIKED_KEY_FORMAT % user.id, 0, 19)]
    users = User.objects.filter(id__in=superlike_list)
    if len(superlike_list) < 20:
        other_count = 20 - len(superlike_list)
        other_users = User.objects.filter(sex=profile.dating_sex,
                                          location=profile.dating_location,
                                          birth_day__gte=min_birth_day,
                                          birth_day__lte=max_birth_day).exclude(id__in=sid_list)[:other_count]
        users = users | other_users
    return users


def like_someone(user, sid):
    '''喜欢某人'''
    Swiped.swipe(uid=user.id, sid=sid, stype='like')

    if Swiped.is_liked(sid, user.id):
        Friend.make_friend(user.id, sid)
        rds.zrem(SUPERLIKED_KEY_FORMAT % user.id, sid)
        return True
    else:
        return False


def superlike_someone(user, sid):
    '''超级喜欢某人'''
    Swiped.swipe(uid=user.id, sid=sid, stype='superlike')

    rds.zadd(SUPERLIKED_KEY_FORMAT % sid, {user.id: time.time()})

    if Swiped.is_liked(sid, user.id):
        Friend.make_friend(user.id, sid)
        rds.zrem(SUPERLIKED_KEY_FORMAT % user.id, sid)
        return True
    else:
        return False


def dislike_someone(user, sid):
    '''不喜欢某人'''
    Swiped.swipe(uid=user.id, sid=sid, stype='dislike')
    rds.zrem(SUPERLIKED_KEY_FORMAT % user.id, sid)


def rewind_swiped(user):
    '''反悔最近一次滑动记录'''
    # 1.反悔次数
    rewind_times = rds.get(REWIND_KEY_FORMAT % user.id, 0)
    if rewind_times >= config.DAILY_REWIND_TIMES:
        raise status.RewindLimitError(msg='滑动超上限')
    # 2.最近一次滑动情况
    latest_swiped = Swiped.objects.filter(uid=user.id).latest('stime')
    now = datetime.datetime.now()
    if (now - latest_swiped.stime).total_seconds() >= config.REWIND_TIMEOUT:
        raise status.RewindTimeOutError(msg='滑动间隔超过指定时间')
    # 3.删除好友关系 / 删除优先推荐队列 / 删除滑动记录 / 更新滑动次数
    # TODO 搜索相关的事务用法和封装
    with transaction.atomic():
        if latest_swiped.stype in ['like', 'superlike']:
            Friend.break_off(user.id, latest_swiped.sid)
        if latest_swiped == 'superlike':
            rds.zrem(SUPERLIKED_KEY_FORMAT % latest_swiped.sid, user.id)
        latest_swiped.delete()

        next_zero = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        remain_seconds = (next_zero - now).total_seconds()
        rds.set(REWIND_KEY_FORMAT % user.id, rewind_times + 1, ex=int(remain_seconds))
