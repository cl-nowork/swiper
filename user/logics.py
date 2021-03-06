import os

import requests

from libs.sms import send_msg
from libs.qn_cloud import upload_to_qn
from commons import keys
from django.core.cache import cache
from swiper import config
from commons.utils import gen_vcode
from tasks import celery_app


def send_vcode(phonenum):
    '''发送短信验证码'''
    # 生成验证码
    vcode = gen_vcode(4)
    print(f'验证码：{vcode}')
    cache.set(keys.VCODE_KEY_FORMAT % phonenum, vcode, 3 * 60)

    resp = send_msg(phonenum, vcode)
    if resp.status_code == 200:
        rst = resp.json()
        if rst['code'] == 200:
            return True
    return False


def get_access_token(code):
    '''获取微博的授权令牌'''
    args = config.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    response = requests.post(config.WB_ACCESS_TOKEN_API, data=args)
    if response.status_code == 200:
        result = response.json()
        return result['access_token'], result['uid']
    return None, None


def get_user_info(access_token, uid):
    '''获取用户的个人信息'''
    args = config.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = uid
    response = requests.get(config.WB_USER_SHOW_API, params=args)
    if response.status_code == 200:
        result = response.json()
        user_info = {
            'ext_uid': 'wb_%s' % uid,
            'nickname': result['name'],
            'sex': 'female' if result == 'f' else 'male',
            'avatar': result['avatar_hd'],
            'location': result['location'].split()[0],
        }
        return user_info
    return None


def save_upload_avatar(user, avatar):
    """本地存储avatar"""
    filename = keys.AVATAR_KEY_FORMAT % user.id
    filepath = f'/tmp/{filename}'
    with open(filepath, 'wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    return filename, filepath


@celery_app.task
def handle_avatar(user, avatar):
    filename, filepath = save_upload_avatar(user, avatar)
    avatar_url = upload_to_qn(filename, filepath)
    user.avatar = avatar_url
    user.save()
    if os.path.exists(filepath):
        os.remove(filepath)
