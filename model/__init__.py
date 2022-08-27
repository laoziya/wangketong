from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app_db(app):
    db.init_app(app)
    # 自动创建数据表，但是这要求你连接数据库的用户有创建权限
    db.create_all(app=app)

from . import user
from . import course
from . import article
from . import user_to_course
from . import tags
from . import comment
from . import comment_to_tag
from . import reply

# from model import user
# from model import course
# from model import article
# from model import user_to_course
# from model import tags
# from model import comment
# from model import comment_to_tag
# from model import reply