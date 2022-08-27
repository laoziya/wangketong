from model import db
import datetime
class Course(db.Model):
    __tablename__ = "course"
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(500))
    image = db.Column(db.String(500))
    CreateAt = db.Column(db.DateTime,default=datetime.datetime.now())
    uid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)

    def keys(self):    
        return ('cid','cname','desc','CreateAt')

    def __getitem__(self, item):
        return getattr(self,item)
# (matching against '^(?:RESTRICT|CASCADE|SET NULL|NO ACTION|SET DEFAULT)$')
