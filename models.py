from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def is_valid_username(cls, username, pwd):
        if not User.query.get(username):
            return bcrypt.generate_password_hash(pwd).decode("utf8")
        else:
            return False
    
    @classmethod
    def is_valid_pwd(cls, username, pwd):
        user = User.query.get(username)
        return bcrypt.check_password_hash(user.password, pwd)

    feedbacks = db.relationship('Feedback')

class Feedback(db.Model):

    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text,
                         db.ForeignKey('users.username'),
                         nullable=False)
    
    user = db.relationship('User')

