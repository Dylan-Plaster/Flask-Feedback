from flask import Flask, render_template, redirect, flash
from models import db, connect_db, User
from forms import RegisterUserForm, LoginUserForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SUPER_$ECRET'

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """Redirect to /register"""
    return redirect('/register')

@app.route('/register', methods=["GET","POST"])
def register():
    """GET: Show a form that when submitted will register a user.
       POST: Handle form submission. Check to make sure username isn't already taken.
             Redirect to /secret when logged in"""


    form = RegisterUserForm()

    if form.validate_on_submit():

        # Get form data:
        username = form.username.data
        password = form.username.data
        email = form.email.data 
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            flash('Username already taken! Please choose another', 'danger')
            return render_template('form.html', form=form)

        return redirect('/secret')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """GET: Show form for logging in. 
       POST: Handle submission of login form, redirect to /secret if user is authenticated """
    form = LoginUserForm()
       


@app.route('/secret')
def secret():
    """Hidden page for logged-in users only"""

