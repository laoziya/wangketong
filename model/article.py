
from model import db
class Article(db.Model):
    __tablename__ = "article"
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_title = db.Column(db.String(50), nullable=False)
    article_fpath = db.Column(db.String(255), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('course.cid', ondelete = "CASCADE"), nullable = False)
    