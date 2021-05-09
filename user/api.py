from commons.keys import VCODE_KEY_FORMAT
from commons.utils import gen_nickname
from django.core.cache import cache
from django.http.response import JsonResponse

from user.logics import send_vcode
from user.models import User
from commons import status

# Create your views here.


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.POST.get('phonenum')
    if not phonenum:
        return JsonResponse({'code': status.INVILD_PATAMS, 'data': None, 'msg': 'phonenum 字段为空'})
    if send_vcode(phonenum):
        return JsonResponse({'code': status.OK, 'data': None, 'msg': '短信发送成功'})
    return JsonResponse({'code': status.VCODE_ERROR, 'data': None, 'msg': '短信发送失败'})


def check_vcode(request):
    '''验证短信码, 登录或者注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cached_vcode = cache.get(VCODE_KEY_FORMAT % phonenum)
    if cached_vcode and vcode and cached_vcode == vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=gen_nickname())
        request.session['uid'] = user.id
        return JsonResponse({'code': status.OK, 'data': user.to_dict(), 'msg': '登录成功'})
    else:
        return JsonResponse({'code': status.INVILID_VCODE, 'data': None, 'msg': '验证码错误'})
