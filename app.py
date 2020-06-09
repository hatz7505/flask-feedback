"""Flask app for Flask-Feedback"""

from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['WTF_CSRF_ENABLED'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "marSHAAAALLLL&&&&haRrrRRrRYyyYY"


@app.route('/')
def redirect_to_register():
    return redirect('/register')


@app.route('/register')
def show_register_form():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/register', methods=["POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = User.is_valid_username(username, pwd)

    if password:
        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        return redirect('/secret') 
    else:
        flash(f"Username {username} already taken")
        return render_template('register.html', form=form)


@app.route('/secret')
def return_text():
    return "You made it!"


@app.route('/login')
def show_login_form():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/login', methods=["POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        
    if User.is_valid_pwd(username, pwd):
        return redirect('/secret') 
    else:
        flash(f"Incorrect username or password")
        return render_template('login.html', form=form)