
from model import db
import datetime
from model.course import Course
from werkzeug.security import generate_password_hash

class UserManager(db.Model):
    __tablename__ = "user"  #映射的数据表，不写的话，默认是类名、
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(128),nullable=False)
    _password = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(128),nullable=False)
    phone = db.Column(db.String(24),nullable=False)
    role = db.Column(db.Enum('0','1'),nullable=False, default='0')
    CreateAt = db.Column(db.DateTime,default=datetime.datetime.now())
    Desc = db.Column(db.String(512))
    # relationship对象不会生效到数据库中
    # 可以通过course属性得到user和course表连接后course中的内容
    # backref='user'可以使course得到属主
    # course = db.relationship("Course", backref='user', userlist=False)
    course = db.relationship("Course", backref='user')

    def keys(self):    
        return ('id','username','email','phone', 'Desc')

    def __getitem__(self, item):
        return getattr(self,item)
    # 属性包装常在属性定义之前，生成两个装饰器@password.setter
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)
    @classmethod
    def create_user(cls, username, password, email, phone, desc=None):
        user = cls()
        user.username = username
        user.password = password
        user.email = email
        user.phone = phone
        user.Desc = desc
        db.session.add(user)
        db.session.commit()
    
app_permission = db.Table("app_permission",
                          db.Column("api_id",db.ForeignKey("api_token.id")),
                          db.Column("permission_id",db.ForeignKey("api_permission.id"))
                          )
# api_token表
#存放的是授权密钥，以及授权id
class ApiToken(db.Model):
    __tablename__ = "api_token"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appid = db.Column(db.String(128), nullable=False)
    secretkey = db.Column(db.String(128), nullable=False)
    #通过中间表去创建多对多的关系
    manage = db.relationship("ApiPermission", secondary=app_permission, backref="token")

#存放的是授权的url
class ApiPermission(db.Model):
    __tablename__ = "api_permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), nullable=False)
    method_type = db.Column(db.String(128), nullable=False)
