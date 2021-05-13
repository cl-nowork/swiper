from commons import status


def need_permission(view_func):
    def check(request, *args, **kwargs):
        perm_name = view_func.__name__
        if request.user.vip.has_perm(perm_name):
            return view_func(request, *args, **kwargs)
        else:
            raise status.PermissionLimitError(msg='权限限制')

    return check
