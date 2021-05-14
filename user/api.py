import logging

from django.core.cache import cache
from django.shortcuts import redirect

from commons import status
from commons.keys import VCODE_KEY_FORMAT, PROFILE_KEY_FORMAT
from commons.utils import gen_nickname
from libs.cache import rds
from swiper import config
from libs.http import render_json
from user import logics
from user.models import User
from user.forms import UserForms, ProfileForms

inf_log = logging.getLogger('inf')


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.POST.get('phonenum')
    if not phonenum:
        raise status.InvildParams(msg='phonenum 字段为空')
    if logics.send_vcode(phonenum):
        return render_json(data=None, msg='短信发送成功')
    raise status.VcodeError(msg='短信发送失败')


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
        inf_log.info(f'User-{user.id} login in')
        request.session['uid'] = user.id
        return render_json(data=user.to_dict(), msg='登录成功')
    else:
        raise status.InvilidVcode(msg='验证码错误')


def wb_auth(request):
    '''微博授权页'''
    return redirect(config.WB_AUTH_URL)


def wb_callback(request):
    '''微博回调接口'''
    code = request.GET.get('code')
    access_token, uid = logics.get_access_token(code)
    if not access_token:
        raise status.AccessTokenError(msg='获取微博access_token失败')
    user_info = logics.get_user_info(access_token, uid)
    if not user_info:
        raise status.UserInfoError(msg='获取微博用户信息失败')
    try:
        user = User.objects.get(ext_uid=user_info['ext_uid'])
    except User.DoesNotExist:
        user = User.objects.create(**user_info)
    request.session['uid'] = user.id
    return render_json(data=user.to_dict(), msg='登录成功')


def get_profile(request):
    '''获取交友资料'''
    key = PROFILE_KEY_FORMAT % request.user.id
    profile_data = rds.get(key)
    if profile_data is None:
        profile_data = request.user.profile.to_dict()
        rds.set(key, profile_data)
    return render_json(data=profile_data, msg='查询成功')


def set_profile(request):
    '''修改交友资料'''
    user_form = UserForms(request.POST)
    profile_form = ProfileForms(request.POST)
    if not user_form.is_valid():
        raise status.UserDataError(data=user_form.errors, msg='参数错误')
    if not profile_form.is_valid():
        raise status.ProfileDataError(data=profile_form.errors, msg='参数错误')
    user = request.user
    user.__dict__.update(user_form.cleaned_data)
    user.save()
    user.profile.__dict__.update(profile_form.cleaned_data)
    user.profile.save()
    return render_json(data=None, msg='更新成功')


def upload_avatar(request):
    '''上传个人头像'''
    avatar = request.FILES.get('avatar')
    logics.handle_avatar.delay(request.user, avatar)
    return render_json(msg='上传成功')
