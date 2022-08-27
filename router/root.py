from flask import Blueprint
from flask import url_for,render_template, request

def index():
    user = {'name': '钱韬', 'age': 20}
    # 渲染函数，用来生成动态页面的
    result = render_template('index.html', content=user)
    return result




root_bp = Blueprint('root', __name__)
root_bp.add_url_rule('/', view_func=index)