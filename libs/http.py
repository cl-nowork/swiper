import json
from django.conf import settings
from django.http import HttpResponse

from commons.status import OK


def render_json(data=None, code=OK, msg=''):
    '''json返回格式'''
    result = {'code': code, 'data': data, 'msg': msg}
    if settings.DEBUG:
        json_result = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_result = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    return HttpResponse(json_result)
