
from flask import url_for,render_template, request
from flask import Blueprint
import json
from libs.response import generate_response
from model.user import UserManager
from model import db


def qt():
    return 'this is qiantao'

def show_userid(user_id):
    return f'user_id is {user_id}'

def geturl():
    # 根据endpoint找url
    result1 = url_for('qt')
    result2 = url_for('show_userid', user_id=666)
    return f'endpoint index2 route is {result1}\n endpoint show_user is {result2}'

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # username = request.args.get('username')
        # password = request.args.get('password')
        if not username or not password:
            return '用户名或密码为空'
        if username=='root' and password=='123456':
            return 'login success'
        return 'login failure'
    return f"用户名：{request.form.get('username')}，密码：{request.form.get('password')}"



def request_test():
    # args = (type(request.args), request.args)
    # req_json = (type(request.json), request.json)
    # req_path = (type(request.path), request.path)
    # req_headers = (type(request.headers), request.headers)


    # result = {"args": args, "json":req_json, "path":req_path, "headers":req_headers}
    # # result = json.loads(result)
    # for key,value in result.items():
    #     print(key, value)
    # return str(result)
    return generate_response(message="get user success")

def add_user():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")
    phone = request.json.get("phone")
    role = request.json.get("role")
    c = username and password and email and phone and role
    if not c:
        return '缺少数据'
    user_info = UserManager(
        username = username,
        password = password,
        email = email,
        phone = phone,
        role = role
    )
    # 或者
    # user_info = UserManager
    # user_info.username = username
    # user_info.password = password
    # user_info.email = email
    # user_info.phone = phone
    # user_info.role = role

    db.session.add(user_info)
    db.session.commit()
    return generate_response(message="add user success")
def delete_user(id):
    del_user = UserManager.query.get(id)
    if del_user:
        db.session.delete(del_user)
        db.session.commit()
        return generate_response(message="delete user success")
    else:
        return generate_response(status_code=10001, message="user not found")
def modify_user(id):
    mod_user = UserManager.query.get(id)
    if mod_user:
        email = request.json.get("email")
        phone = request.json.get("phone")
    mod_user.email = email
    mod_user.phone = phone
    db.session.add(mod_user)
    db.session.commit()
    return generate_response(message="modify user success")

    


stu_bp = Blueprint('stu', __name__, url_prefix="/v1")
stu_bp.add_url_rule("/qt", view_func=qt)
stu_bp.add_url_rule('/user/<int:user_id>', view_func=show_userid)
stu_bp.add_url_rule('/urlfor', view_func=geturl)
stu_bp.add_url_rule('/login', view_func=login, methods=['POST', 'GET'])
stu_bp.add_url_rule('/req', view_func=request_test)
stu_bp.add_url_rule('/reg', view_func=add_user, methods=["GET", 'POST'])
stu_bp.add_url_rule('/delete/<int:id>', view_func=delete_user,methods=["DELETE"])
stu_bp.add_url_rule('/mod/<int:id>', view_func=modify_user)


