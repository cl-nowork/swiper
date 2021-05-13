from qiniu import Auth, put_file

from swiper import config


def upload_to_qn(filename, filepath):
    """上传文件到七牛云"""
    q = Auth(config.QN_ACCESSKEY, config.QN_SECRETKEY)
    token = q.upload_token(config.QN_BUCKETNAME, filename, 3600)
    put_file(token, filename, filepath)
    avatar_url = f'{config.QN_BASE_URL}/{filename}'
    return avatar_url
