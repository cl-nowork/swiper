''''程序逻辑中的状态码'''

OK = 0


class LogicError(Exception):
    code = None
    data = None
    msg = ''

    def __init__(self, data=None, msg=''):
        self.data = data
        self.msg = msg


def gen_logic_error(name, code):
    return type(name, (LogicError, ), {'code': code})


InvildParams = gen_logic_error('InvildParams', 999)
VcodeError = gen_logic_error('VcodeError', 1000)
InvilidVcode = gen_logic_error('InvilidVcode', 1001)
AccessTokenError = gen_logic_error('AccessTokenError', 1002)
UserInfoError = gen_logic_error('UserInfoError', 1003)
NoLoginError = gen_logic_error('NoLoginError', 1004)
UserDataError = gen_logic_error('UserDataError', 1005)
ProfileDataError = gen_logic_error('ProfileDataError', 1006)
SwipeRepeatError = gen_logic_error('SwipeRepeatError', 1007)
RewindLimitError = gen_logic_error('RewindLimitError', 1008)
RewindTimeOutError = gen_logic_error('RewindTimeOutError', 1009)
PermissionLimitError = gen_logic_error('PermissionLimitError', 1010)
