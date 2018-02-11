from . import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255), index=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True,index=True)
    bio = db.Column(db.String(255))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    #blogs = db.relationship('Blog',backref='author',lazy='dynamic')
    confirmed = db.Column(db.Boolean,default=False)


    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
 
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
        

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'{self.username}'

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)


# class Blog(db.Model):
#     __tablename__='blogs'
#     id = db.Column(db.Integer,primary_key=True)
#     body = db.Column(db.Text)
#     timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)
#     author_id= db.Column(db.Integer,db.ForeignKey('users.id'))