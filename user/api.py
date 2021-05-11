from commons import status
from commons.keys import VCODE_KEY_FORMAT
from commons.utils import gen_nickname
from django.core.cache import cache
from django.shortcuts import redirect
from swiper import config
from libs.http import render_json
from user import logics
from user.models import User
from user.forms import UserForms, ProfileForms

# Create your views here.


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.POST.get('phonenum')
    if not phonenum:
        return render_json(code=status.INVILD_PATAMS, data=None, msg='phonenum 字段为空')
    if logics.send_vcode(phonenum):
        return render_json(data=None, msg='短信发送成功')
    return render_json(code=status.VCODE_ERROR, data=None, msg='短信发送失败')


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
        return render_json(data=user.to_dict(), msg='登录成功')
    else:
        return render_json(code=status.INVILID_VCODE, data=None, msg='验证码错误')


def wb_auth(request):
    '''微博授权页'''
    return redirect(config.WB_AUTH_URL)


def wb_callback(request):
    '''微博回调接口'''
    code = request.GET.get('code')
    access_token, uid = logics.get_access_token(code)
    if not access_token:
        return render_json(status.ACCESS_TOKEN_ERROR, data=None, msg='获取微博access_token失败')
    user_info = logics.get_user_info(access_token, uid)
    if not user_info:
        return render_json(code=status.USER_INFO_ERROR, data=None, msg='获取微博用户信息失败')
    try:
        user = User.objects.get(ext_uid=user_info['ext_uid'])
    except User.DoesNotExist:
        user = User.objects.create(**user_info)
    request.session['uid'] = user.id
    return render_json(data=user.to_dict(), msg='登录成功')


def get_profile(request):
    '''获取交友资料'''
    profile_data = request.user.profile.to_dict()
    return render_json(data=profile_data, msg='查询成功')


def set_profile(request):
    '''修改交友资料'''
    user_form = UserForms(request.POST)
    profile_form = ProfileForms(request.POST)
    if not user_form.is_valid():
        return render_json(code=status.USER_DATA_ERROR, data=user_form.errors, msg='参数错误')
    if not profile_form.is_valid():
        return render_json(code=status.PROFILE_DATA_ERROR, data=profile_form.errors, msg='参数错误')
    user = request.user
    user.__dict__.update(user_form.cleaned_data)
    user.save()
    user.profile.__dict__.update(profile_form.cleaned_data)
    user.profile.save()
    return render_json(data=None, msg='更新成功')


def upload_avatar(request):
    '''上传个人头像'''
    return render_json({})