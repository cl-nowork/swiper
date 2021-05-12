from social import logics
from libs.http import render_json
from social.models import Swiped
from user.models import User


def get_rcmd_users(request):
    """获取推荐用户"""
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(result, msg='查询成功')


def like(request):
    '''右滑, 喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.user, sid)
    return render_json({'matched': is_matched}, msg='success')


def superlike(request):
    '''上滑, 超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.user, sid)
    return render_json({'matched': is_matched}, msg='success')


def dislike(request):
    '''左滑, 不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.user, sid)
    return render_json(msg='success')


def who_liked_me(request):
    '''查看都有谁喜欢过我'''
    like_me_ids = Swiped.who_liked_me(request.user.id)
    users = User.objects.filter(id__in=like_me_ids)
    result = [user.to_dict() for user in users]
    return render_json(result, msg='success')
