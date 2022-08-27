
from model import db
import datetime


class Reply(db.Model):
    __tablename__ = "reply"
    replyid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reply_content = db.Column(db.String(500), nullable=False)
    CreateAt = db.Column(db.DateTime,default=datetime.datetime.now())
    level = db.Column(db.Integer, nullable=False)
    commentid = db.Column(db.Integer, db.ForeignKey('comment.commentid', ondelete = "CASCADE"), nullable = False)