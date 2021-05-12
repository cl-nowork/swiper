''''程序逻辑中的状态码'''

OK = 0


class LogicError(Exception):
    code = None

    def __init__(self, data=None, msg=''):
        self.data = data
        self.msg = msg


def gen_logic_error(name, code):
    return type(name, (LogicError, ), {'code': code})


InvildParams = gen_logic_error('InvildParams', 999)
VcodeError = gen_logic_error('VcodeError', 1000)
InvilidVcode = gen_logic_error('InvilidVcode', 1001)
AccessTokenError = gen_logic_error('AccessTokenError', 1002)
UserInfoError = gen_logic_error('UserInfoError', 1002)
NoLoginError = gen_logic_error('NoLoginError', 1002)
UserDataError = gen_logic_error('UserDataError', 1003)
ProfileDataError = gen_logic_error('ProfileDataError', 1004)
SwipeRepeatError = gen_logic_error('SwipeRepeatError', 1005)
SwipeParamsError = gen_logic_error('SwipeParamsError', 1005)