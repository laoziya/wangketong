
from model import db

class Comment_to_tag(db.Model):
    __tablename__='commet_to_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commentid = db.Column(db.Integer, db.ForeignKey('comment.commentid', ondelete = "CASCADE"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id', ondelete = "CASCADE"), nullable=False)
