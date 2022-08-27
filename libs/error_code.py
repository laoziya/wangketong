from email import message
from werkzeug.exceptions import HTTPException

from model.user import ApiPermission

class APIException(HTTPException):
    code = 200
    message = "opps!"
    status_code = 9999
    def __init__(self, message=None, code=None, status_code = None):
        if message:
            self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        super(APIException, self).__init__()
    def get_body(
        self,
        environ = None,
        scope = None,
    ) -> str:
        body = dict(
            message = self.message,
            status_code = self.status_code
        )
        import json
        content = json.dumps(body)
        return content

    def get_headers(
        self,
        environ = None,
        scope = None,
    ) :
        return [('content-Type', 'application/json')]

class APIAuthorizedException(APIException):
    message = "API授权认证失败"
    status_code = 10002
    code = 401

class FormValidateException(APIException):
    message = "表单验证失败"
    status_code = 10003

class TokenFailException(APIException):
    message = "token不合法，验证失败"
    status_code = 10005

# 登录失败
class LoginFail(APIException):
    message="登录失败"
    status_code = 1006
    # code = 405

# 注册失败
class RegisterFali(APIException):
    message="注册失败"
    status_code=1007