import datetime

from user.models import User
from social.models import Swiped, Friend


def rcmd(user):
    """推荐可滑动的用户"""
    profile = user.profile
    today = datetime.datetime.now()

    min_birth_day = today - datetime.timedelta(profile.max_dating_age * 365)
    max_birth_day = today - datetime.timedelta(profile.min_dating_age * 365)

    sid_list = Swiped.objects.filter(uid=user.id).values_list('id', flat=True)

    users = User.objects.filter(
        sex=profile.dating_sex,
        location=profile.dating_location,
        birth_day__gte=min_birth_day,
        birth_day__lte=max_birth_day
    ).exclude(id__in=sid_list)[:20]
    return users


def like_someone(user, sid):
    '''喜欢某人'''
    Swiped.objects.create(uid=user.id, sid=sid, stype='like')

    if Swiped.is_liked(sid, user.id):
        Friend.make_friend(user.id, sid)
        return True
    else:
        return False
