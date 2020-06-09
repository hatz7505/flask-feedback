"""Flask app for Flask-Feedback"""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

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
    if 'username' in session:
        username = session['username']
        return redirect(f'/secret/users/{username}')
    else:
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
    else:
        return render_template('register.html', form=form)

    if password:
        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        return redirect(f'/secret/users/{username}')
    else:
        flash(f"Username {username} already taken")
        return render_template('register.html', form=form)

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
    else:
        return render_template('login.html', form=form)

    if User.is_valid_pwd(username, pwd):
        session['username'] = form.username.data
        return redirect(f'/secret/users/{username}')
    else:
        flash(f"Incorrect username or password")
        return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/register')

@app.route('/secret/users/<username>')
def show_user(username):
    if "username" not in session:
        flash('Please login')
        return redirect('/login')
    else:
        user = User.query.get(username)
        return render_template('secret.html', user=user)

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    form = FeedbackForm()
    if 'username' in session:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/secret/users/{username}')
        else:
            return render_template('feedback.html', form=form)
    else:
        flash('Please login')
        return redirect('/login')

@app.route('/feedback/<int:id>/update/')
def update_feedback_form(id):
    name = session['username']
    feedback_author = Feedback.query.get(id).user.username
    user_feedback = Feedback.query.get(id)
    # fix variable names

    form = FeedbackForm(obj=user_feedback)

    if name == feedback_author:
        return render_template('update_feedback.html',form=form)
    else:
        flash('What are you trying to do??????')
        return redirect(f'/secret/users/{name}')

@app.route('/feedback/<int:id>/update/', methods=["POST"])
def update_feedback(id):
    feedback = Feedback.query.get(id)
    name = session['username']
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback was added! Thank you')
        return redirect(f'/secret/users/{name}')
    else:
        return redirect('/')
