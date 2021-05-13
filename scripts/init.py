import os
import sys
import random
from datetime import date

import django

# 加载django环境
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
django.setup()

from user.models import User


# !/usr/bin/env python

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤何'
    '吕施张孔曹严华金魏陶姜戚谢邹喻柏水胡凌霍'
    '窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任'
    '袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝强'
    '邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄麻'
    '计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵'
    '贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田'
)

first_names = {
    'male': [
        '炫迁', '铭晋', '胜池', '信磊', '峻越', '谦元', '海钟', '任元', '冰朋', '韶然', '祺旷', '宁靖', '奥若', 
        '钟涛', '苛勤', '含棕', '宏羽', '肃义', '望卫', '健轩', '皓南', '文谦', '苛敬', '圣渊', '聪闻', '彰豫', 
        '原鸿', '乐洋', '昆文', '基飘', '妙茂', '方勉', '昭善', '恒昆', '擎利', '意楷', '商虎', '卫圆', '肖钟', 
        '波向', '群乐', '惜石', '尘生', '信星', '博卡', '伟悟', '茂松', '鸣利', '神实', '际永', '余民', '渊旷'
    ],
    'female': [
        '惠睿', '晴茜', '岚嫦', '云涵', '晴惠', '怡翎', '裕梅',
        '涵惠', '惠絮', '涵菡', '雯婷', '寒淑', '润洁', '秉文',
        '晴清', '淑涵', '珺涵', '云华', '舒媛', '素娅', '花曼',
        '岚雅', '清华', '寒菊', '涵茵', '岚菡', '欣琳', '熙玉',
        '岚菲', '寒云', '茹絮', '寒媛', '岚瑜', '正妍', '琳竣',
        '淑淑', '惠语', '寒华', '涵婷', '晴珺', '妍如', '榕嫣',
        '寒瑜', '云嫦', '茵清', '茵嫣', '惠云', '洁玲', '雨蓉',
        '翔雯', '淑梦', '晴菡', '珺云', '清雅', '梓婧', '雯婧',
        '雯嘉', '雯舒', '茜菡', '云嫣', '清梦', '秀珊', '欣怡',
        '惠茜', '茜华', '茜茜', '舒菲', '婷雯', '晓悦', '芷秀',
        '欣瑶', '曦秀', '婷丽', '莉娜', '东玲', '巧娜', '佳艳',
        '秀秀', '新颖', '依娜', '欣瑶', '梦洁', '菁茹', '泽芳',
        '怡若', '陈红', '婧宁', '美怡', '悦帆', '莹莹', '莉绫',
        '德梅', '燕萍', '瑛蔓', '鹤梅', '蓉华', '佳莉', '蔡琳',
        '婧妍', '斯玉', '恺玲', '珂妍', '小莉', '成美', '倩冰'
    ]
}


def random_name():
    """随机取一个名字"""
    last_name = random.choice(last_names)
    sex = random.choice(list(first_names.keys()))
    first_name = random.choice(first_names[sex])
    return ''.join([last_name, first_name]), sex


def create_robots(n):
    """创建初始用户"""
    for i in range(n):
        name, sex = random_name()
        year = random.randint(1970, 2008)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        try:
            user = User.objects.create(
                phonenum=random.randint(20000000000, 29999999999),
                nickname=name,
                sex=sex,
                birth_day=date(year, month, day),
                location=random.choice([item[0] for item in User.LOCATION]),
            )
            print(f'created: {user.id} {name} {sex}')
        except django.db.utils.IntegrityError:
            pass


if __name__ == '__main__':
    create_robots(10000)
