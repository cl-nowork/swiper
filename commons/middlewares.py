from django.utils.deprecation import MiddlewareMixin
from user.models import User
from commons import status
from libs.http import render_json


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
            raise status.NoLoginError(msg='需要登录')
        request.user = User.objects.get(id=uid)


class LogicErrorMiddleware(MiddlewareMixin):
    '''逻辑错误中间件'''

    def process_exception(self, request, exception):
        if isinstance(exception, status.LogicError):
            return render_json(code=exception.code, data=exception.data, msg=exception.msg)
