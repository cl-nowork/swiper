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


class App:
    def __init__(self):
        self.li = []

    def route(self):
        def add_url(x):
            self.li.append(x)
            print(self.li)
        return add_url


global_num = 10

def _add():
    # global_num += 1
    print(global_num)