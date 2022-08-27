from model import db
from model.user import UserManager
from model.course import Course
import datetime
class User_to_course(db.Model):
    __tablename__='user_to_course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, db.ForeignKey('course.cid', ondelete="CASCADE"), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    CreateAt = db.Column(db.DateTime,default=datetime.datetime.now())
    user = db.relationship("UserManager", backref='m')
    course = db.relationship('Course', backref='m')