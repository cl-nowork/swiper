from social import logics
from libs.http import render_json


def get_rcmd_users(request):
    """获取推荐用户"""
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(result, msg='查询成功')
