from model import db
import datetime

class Comment(db.Model):
    __tablename__ = "comment"
    commentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(500), nullable=False)
    picture_fpath = db.Column(db.String(255))
    CreateAt = db.Column(db.DateTime,default=datetime.datetime.now())
    aid = db.Column(db.Integer, db.ForeignKey('article.aid', ondelete = "CASCADE"), nullable = False)