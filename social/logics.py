import time
import datetime

from user.models import User
from social.models import Swiped, Friend
from libs.cache import rds
from commons.keys import SUPERLIKED_KEY_FORMAT


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
