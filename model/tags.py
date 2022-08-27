
from model import db

class Tags(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(100), nullable=False)
    aid = db.Column(db.Integer, db.ForeignKey('article.aid', ondelete = "CASCADE"), nullable=False)