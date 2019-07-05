from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    
    
    def __init__(self, username, password):
        self.id = _id                               ## avoid using python keyword id
        self.username = username
        self.password = password
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    
    @classmethod                ## use a current class instead hard-coding 
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        
    @classmethod                ## use a current class instead hard-coding 
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()