from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from user.models import User
from commons import status


class AuthorizeMiddleware(MiddlewareMixin):
    '''登录中间件'''
    WHITE_LIST = [
        '/v1/users/get_vcode/',
        '/v1/users/check_vcode/',
        '/v1/users/wb_auth/',
        '/v1/users/wb_callback/',
    ]

    def process_request(self, request):
        if request.path in self.WHITE_LIST:
            return
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': status.NO_LOGIN_ERROR, 'data': None, 'msg': '需要登录'})
        request.user = User.objects.get(id=uid)
