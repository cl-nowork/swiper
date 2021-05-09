import time
import hashlib
import requests
from swiper.config import WANGYI_API, WANGYI_APP_KEY, WANGYI_APP_SECRET, WANGYI_Nonce


def send_msg(phone, vcode):
    cur_time = str(int(time.time()))
    raw_str = WANGYI_APP_SECRET + WANGYI_Nonce + cur_time
    check_sum = hashlib.sha1(raw_str.encode('utf8')).hexdigest()
    data = {
        'mobile': phone,
        'authCode': vcode
    }
    headers = {
        'AppKey': WANGYI_APP_KEY,
        'Nonce': WANGYI_Nonce,
        'CurTime': cur_time,
        'CheckSum': check_sum,
    }
    resp = requests.post(WANGYI_API, data=data, headers=headers, verify=False)
    return resp


if __name__ == '__main__':
    resp = send_msg(17682808212)
    pass
