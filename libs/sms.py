import hashlib
import time

import requests
from swiper.config import (WANGYI_API, WANGYI_APP_SECRET, WANGYI_HEADERS,
                           WANGYI_Nonce)


def send_msg(phone, vcode):
    cur_time = str(int(time.time()))
    raw_str = WANGYI_APP_SECRET + WANGYI_Nonce + cur_time
    check_sum = hashlib.sha1(raw_str.encode('utf8')).hexdigest()
    data = {
        'mobile': phone,
        'authCode': vcode
    }
    req_headers = WANGYI_HEADERS.copy()
    req_headers['CurTime'] = cur_time
    req_headers['CheckSum'] = check_sum
    resp = requests.post(WANGYI_API, data=data, headers=req_headers, verify=False)
    return resp


if __name__ == '__main__':
    resp = send_msg(17682808212)
    pass
