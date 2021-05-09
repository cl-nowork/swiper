from libs.sms import send_msg
from commons.keys import VCODE_KEY_FORMAT
from django.core.cache import cache
from commons.utils import gen_vcode


def send_vcode(phonenum):
    '''发送短信验证码'''
    # 生成验证码
    vcode = gen_vcode(4)
    print(f'验证码：{vcode}')
    cache.set(VCODE_KEY_FORMAT % phonenum, vcode, 3 * 60)

    resp = send_msg(phonenum, vcode)
    if resp.status_code == 200:
        rst = resp.json()
        if rst['code'] == 200:
            return True
    return False
