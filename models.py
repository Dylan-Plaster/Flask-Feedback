"""Models for flask-feedback app"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt, check_password_hash


db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.String, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    posts = db.relationship('Feedback', backref=backref('user', cascade="all, delete"))

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password and return user object"""

        hashed = bcrypt.generate_password_hash(password)
        # this returns a bytestring, need to convert to unicode string:
        hashed_utf8 = hashed.decode("utf8")

        user =  cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that the user exists and the password is correct
        
        Return user if valid, otherwise return False"""

        u = User.query.filter_by(username=username).first()


        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"))



