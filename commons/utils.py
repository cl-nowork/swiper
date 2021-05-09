import random


def gen_vcode(num):
    '''产生指定长度的随机数字符串'''
    chars = [str(random.randint(0, 9)) for _ in range(num)]
    return ''.join(chars)


def gen_nickname():
    '''生成昵称'''
    # TODO
    return '这个人很懒'
