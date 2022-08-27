


from ast import keyword
from os import times
import time
from flask import Blueprint, request, Response
from libs.auth import auth, create_salt
from libs.response import generate_response
from model import db
from model.user import UserManager
from libs.userControl import User
from model.course import Course
from sqlalchemy import or_
from flask_restful import Resource, Api
from hashlib import md5
from model.user_to_course import User_to_course
from libs.error_code import TokenFailException, LoginFail
from libs.handle import default_error_handler


# 用户注册处理函数
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    phone = request.form.get('phone')
    Desc = request.form.get('desc')
    # 判断用户是否已存在
    user_exists = UserManager.query.filter(or_(
        UserManager.phone==phone,
        UserManager.email==email,
    )).first()
    if user_exists:
        return generate_response(status_code='10001', message='user exists')
    # 添加新用户
    user = UserManager()
    if username and password and email and phone:
        if Desc:
            UserManager.create_user(username, password, email, phone, Desc)
        else:
            UserManager.create_user(username, password, email, phone)
    else:
        return generate_response(status_code='10001', message='error, Missing parameter')
    return generate_response(message='register success')

# 用户登录
def login():
    password = request.form.get('password')
    account = request.form.get('account')
    print(request.form)
    # 判断输入不为空，并判断登录方式（电话号码登录或邮件登录）
    if not account or not password:
        raise LoginFail
    user = UserManager.query.filter(or_(
        UserManager.phone==account,
        UserManager.email==account
    )).first()
    # 判断是否有此用户
    if not user:
        raise LoginFail
    # 验证密码，验证成功生成一个User对象
    if user.password == password:
        user_obj = User(user.username, user.password, user.email, user.phone, user.role)
        if user.Desc:
            user_obj.Desc = user.Desc
        uid = str(user.id)
        salt = create_salt()
        passwd = user.password
        timestamp = str(time.time())
        raw = uid+salt+passwd+timestamp
        m1 = md5()
        m1.update(raw.encode(encoding='utf-8'))
        sign = m1.hexdigest()

        # resp = Response(result)
        # resp.content_type = 'json'
        # # print(dir(resp))
        # resp.delete_cookie("uid")
        # resp.set_cookie("uid", uid)
        # resp.delete_cookie("salt")
        # resp.set_cookie("salt", salt)
        # resp.delete_cookie("sign")
        # resp.set_cookie("sign", sign)
        # resp.delete_cookie("timestamp")
        # resp.set_cookie("timestamp", timestamp)
        # # return resp
        result = generate_response(message='login success')
        # result['cookie'] = f"uid={uid}; salt={salt}; sign={sign}; timestamp={timestamp}"
        result['uid']=uid
        result['salt']=salt
        result['sign']=sign
        result[timestamp]=timestamp
        return result
    else:
        raise LoginFail

# #数据验证  wtforms
# class LoginView(Resource):
#     def post(self):
#         data = request.json
#         form = LoginForm(data=data)
#         user = form.validate()
#         if user:
#             #验证通过，生成token
#             token = create_token(user.id)
#             return generate_response(data={"token":token})
#         else:
#             return generate_response(message=form.errors)

# api.add_resource(LoginView, "/login")


class UserView(Resource):
    # 查询用户
    def get(self, id=None):
        if id:
            user = UserManager.query.get(id)
            if user:
                return generate_response(message='user query success', data=dict(user))
            else:
                return generate_response(status_code='1001', message='user not found')
        keyword = request.args.get('keyword')
        if keyword:
            user_lst = UserManager.query.filter(or_(
            UserManager.username.like(f"%%{keyword}%%"),
            UserManager.email==keyword,
            UserManager.phone==keyword
            )).all()
            return generate_response(message='user query success', data=[dict(user) for user in user_lst])
        return 'current user'
    # 修改用户名和描叙
    @auth
    def put(self):
        username = request.form.get('username')
        desc = request.form.get('desc')
        id = request.cookies.get('uid')
        user = UserManager.query.get(id)
        msg = 'user msg mod success'
        status_code = 10000
        if username:
            if username != user.username:
                user.username = username
            else:
                msg = 'not modify'
                status_code = 10001
        if desc:
            if desc != user.Desc:
                user.Desc = desc
            else:
                msg = 'not modify'
                status_code = 10001
        db.session.add(user)
        db.session.commit()
        return generate_response(status_code=status_code, message=msg)
    # 删除用户
    @auth
    def delete (self, id):
        return 'this is delete'


user_bp = Blueprint('user', __name__, url_prefix="/api/user")
user_bp.add_url_rule('/reg', view_func=register, methods=['POST'])
user_bp.add_url_rule('/login', view_func=login, methods=['POST'])
user_api = Api(user_bp)
#设置异常返回标准化
user_api.handle_error = default_error_handler

# user_api.decorators([auth])
# 操作用户
user_api.add_resource(UserView, '/')
user_api.add_resource(UserView, '/<int:id>', endpoint='user_api_p')



