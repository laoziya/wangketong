from wtforms import Form, StringField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError
from model.user import UserManager
from model import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserForm(Form):
    # 变量名需要和客户端传递的字段名一致
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email(message="邮箱不合法")])
    _password = StringField(validators=[DataRequired(), Regexp(r'\w{6,18}', message="密码不符合要求")])
    phone = StringField(validators=[DataRequired(), Regexp(r'1\d{10}',message="电话不符合要求+")])

    #自定义验证器，验证邮箱是否唯一
    #自定义检查字段 方法名：validate_你要检查的字段
    def validate_email(self, value):
        if UserManager.query.filter_by(email = value.data).first():
            raise ValidationError("邮箱已存在")

    def validate_name(self, value):
        #对数据进行修改，给客户端传进来的所有用户名都加一个sanchuang-开头
        value.data = "sanchuang-" + value.data
    @property  # -----> password.setter
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    @classmethod
    def create_user(cls, username, userpass, useremail, usermobile):
        user = cls()
        user.username = username
        user.password = userpass
        user.useremail = useremail
        user.usermobile = usermobile
        db.session.add(user)
        db.session.commit()

class LoginForm(Form):
    userName = StringField(validators=[DataRequired(), Email(message="邮箱不合法")])
    password = StringField(validators=[DataRequired(), Regexp(r'\w{6,18}', message="密码不符合要求")])

    def validate(self):
        super().validate()
        if self.errors:
            return False
        user = UserManager.query.filter_by(useremail =self.userName.data).first()
        if user and check_password_hash(user.password, self.password.data):
            return user
        else:
            raise ValidationError("验证失败！")
