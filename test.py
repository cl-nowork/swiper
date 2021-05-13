from django.db import transaction
from user.models import User


def test():
    with transaction.atomic():
        User.objects.create(
            phonenum=333333333,
            nickname='test1',
            sex='female',
            location='浙江',
        )
        raise ValueError('xxxxxxxx')
        User.objects.create(
            phonenum=66666666,
            nickname='test2',
            sex='female',
            location='浙江',
        )
