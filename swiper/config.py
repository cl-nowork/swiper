from urllib.parse import urlencode

# redis 配置
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 3
}

# 七牛云对象存储
QN_ACCESSKEY = 'D3F_KQg_fm1jjGKN3kj3FhPIErNl09s7fA6cn9MA'
QN_SECRETKEY = '4JhpHsUeG4m2BZevuMGX8L2v60nqzXgeLJRN-cEI'
QN_BUCKETNAME = 'swiper-cl'
QN_BASE_URL = 'http://qsxntfzyk.hd-bkt.clouddn.com'

# 网易短信
WANGYI_API = 'http://api.netease.im/sms/sendcode.action'
WANGYI_APP_KEY = 'a6185afcb1063709d1aa1e25f03757e6'
WANGYI_APP_SECRET = '108a1d831424'
WANGYI_Nonce = 'xxxxxx'
WANGYI_HEADERS = {
    'AppKey': WANGYI_APP_KEY,
    'Nonce': WANGYI_Nonce,
    'CurTime': None,
    'CheckSum': None,
}


# 微博第三方平台登录
WB_APPKEY = '1769539323'
WB_APPSECRET = 'd95794ea51df085b1bb4a04fb19a0d7e'
WB_CALLBACK = 'http://127.0.0.1:8000/v1/users/wb_callback'
# 1. Authorize接口
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_ARGS = {
    'client_id': WB_APPKEY,
    'redirect_uri': WB_CALLBACK,
    'display': 'default'
}
WB_AUTH_URL = f'{WB_AUTH_API}?{urlencode(WB_AUTH_ARGS)}'
# 2. Access_Token接口
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_ARGS = {
    'client_id': WB_APPKEY,
    'client_secret': WB_APPSECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WB_CALLBACK,
    'code': None
}
# 3. user_show接口
WB_USER_SHOW_API = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_ARGS = {
    'access_token': None,
    'uid': None
}
