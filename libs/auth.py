from flask import redirect, url_for, current_app
from model.user import UserManager
from libs.response import generate_response
from functools import wraps
from hashlib import md5
from model.user import ApiToken
import time
from random import Random
from libs.error_code import APIAuthorizedException
from itsdangerous import TimedJSONWebSignatureSerializer as TJS
from itsdangerous import BadSignature, SignatureExpired
from libs.error_code import TokenFailException



from flask import request

def auth_api():
    params = request.cookies
    appid = params.get("uid")
    salt = params.get("salt") #盐值
    sign = params.get("sign") #签名
    timestamp = params.get("timestamp") #时间戳

    if time.time() - int(timestamp) >600:
        return False

    # api_token = ApiToken.query.filter_by(appid = appid).first()
    user = UserManager.query.filter(UserManager.id==appid).first()
    # if not api_token:
    #     return False
    if not user:
        return False

    #验证有没有此url和方法的权限
    # if not has_permission(api_token, request.path, request.method.lower()):
    #     return False
    #获取数据库里的密钥
    # secretkey = api_token.secretkey
    secretkey = user.password
    #生成服务端的签名
    #可以加上时间戳来防止签名被别人盗取，重复访问
    user_sign = appid + salt + secretkey + timestamp
    # user_sign = appid + salt + secretkey
    m1 = md5()
    m1.update(user_sign.encode(encoding="utf-8"))
    #判断客户端传递过来的签名和服务端生成签名是否一致
    if sign != m1.hexdigest():
        #raise AuthFailException
        return False
    else:
        return True

#url验证
#192.168.2.152:9000/stuapi  GET
def has_permission(api_token, url, method):
    #客户端请求的方法和url
    #get/stuapi
    mypermission = method+url
    #获取此api_token对象的所有url权限
    all_permission = [permission.method_type+permission.url
                      for permission in api_token.manage]
    if mypermission in all_permission:
        return True
    else:
        return False


# 自定义权限认证装饰器
def auth(func):
    # 保留装饰的函数元数据，如函数名，保证endpoin不一样
    @wraps(func)
    def inner(*args, **kwargs):
        if auth_api():
            result = func(*args, **kwargs)
            return result
        else:
            raise APIAuthorizedException
            # return generate_response(status_code=1001, message='no login')
    return inner


# 获取由4位随机大小写字母、数字组成的salt值
def create_salt(length=4):
  salt = ''
  chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
  len_chars = len(chars) - 1
  random = Random()
  for i in range(length):
    # 每次从chars中随机取一位
    salt += chars[random.randint(0, len_chars)]
  return salt



  #https
#加时间戳
#JWT JWS JWE
#https://www.jianshu.com/p/50ade6f2e4fd
#生成token
def create_token(uid):
    #第一个参数传递内部私钥,测试环境写死
    #第二个参数是有效期
    s = TJS(current_app.config["SECRET_KEY"], expires_in=current_app.config["EXPIRES_IN"])
    #s = TJS("123456", expires_in=10)
    token = s.dumps({"uid":uid}).decode("ascii")
    return token


def verify_token(token):
    s = TJS(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token)
    except BadSignature:
        print("xxxxxxxxxxxxxxxx")
        raise TokenFailException
    except SignatureExpired:
        raise RuntimeError("token过期")
    return data
