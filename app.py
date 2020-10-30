from flask import Flask, render_template, redirect, flash, session, Markup
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
import traceback, sys


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SUPER_$ECRET'

connect_db(app)
# db.drop_all()
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
        password = form.password.data
        email = form.email.data 
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        try:
            db.session.commit()
            session['username'] = user.username
        except IntegrityError as e:

            # Turn the exception into a string
            string = str(e)

            # Check which kind of integrity error is raised to see if the username or email is a duplicate:
            if "DETAIL:  Key (username)" in string:
                flash('Username already taken! Please choose another', 'danger')
            elif "Key (email)" in string:
                flash(Markup('There is already an account associated with this email address. Please <a href="/login" class="alert-link">Login</a> '), 'danger')

            
            
            return render_template('form.html', form=form, message="Register new user:")

        return redirect(f'/users/{user.username}')
    else:
        return render_template('form.html', form=form, message="Register new user:")



@app.route('/login', methods=["GET", "POST"])
def login():
    """GET: Show form for logging in. 
       POST: Handle submission of login form, redirect to /secret if user is authenticated """


    form = LoginUserForm()

    if form.validate_on_submit():

        # Get form data
        username = form.username.data
        password = form.password.data

        # Authenticate user
        user = User.authenticate(username=username, password=password)
        
        if user: 
            session["username"] = username # keep user logged in
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Username/Password not recognized"]
            # return render_template("form.html", form=form, message="Login:")

    
    return render_template("form.html", form=form, message="Login:")
        

       

@app.route('/users/<username>')
def user_details(username):
    """Logged in users only. Show user details and feedback posts"""
    if "username" not in session:
        flash("You must be logged in to view this page!", 'danger')
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        posts = user.posts
        return render_template('user_details.html', user=user, posts=posts)


@app.route('/logout')
def logout():
    """Logout a user. Clear the session. Redirect to home"""
    session.pop("username", None)
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def feedback(username):

    """GET: Display form to create a new piece of feedback
       POST: Handle form submission. Create new feedback post.
       Redirect to /users/username. Make sure only the user who is logged in can add feedback"""

    if "username" not in session:
        flash("You must be logged in to view this page", 'danger')
        return redirect('/login')
    else:
       form = FeedbackForm()

       if form.validate_on_submit():

           # Get form data
           title = form.title.data 
           content = form.content.data

           # Create new feedback post in database 
           feedback = Feedback(title=title, content=content, username=username)

           db.session.add(feedback)
           db.session.commit()

           return redirect(f'/users/{username}') 


       else:
           return render_template('feedback_form.html', form=form)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Delete a user. Remove them from the database, delete all of their feedback posts,
       and clear anhy info in the flask session. Redirect to /"""

        # Make sure user is logged in. If not, redirect home
    if "username" not in session:
        flash("You must be logged in to do that!", 'danger')
        return redirect('/login')

        # If the user is logged in, get their user model and delete it
    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()

        session.pop("username", None)
        return redirect('/')



@app.route('/feedback/<feedback_id>/update', methods=["GET","POST"])
def edit_feedback(feedback_id):
    """Display a form to edit feedback. Make sure that only the user who wrote the post can access this form"""

    # Get the post to edit
    feedback = Feedback.query.get_or_404(feedback_id)

    # Make sure only the creator of the post can edit:
    if "username" not in session:
        flash("You must be logged in to do that!", 'danger')
        return redirect('/login')
    elif session['username'] != feedback.user.username:
        flash("You are not authorized to update that post", 'danger')
        return redirect('/login')

    # If the user is correct, display the edit form:
    else:
        form = FeedbackForm(obj=feedback)

        # When the form is submitted, get the form data
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback.title = title
            feedback.content = content

            db.session.commit()

            return redirect(f'/users/{feedback.user.username}')


        return render_template('feedback_form.html', form=form)

@app.route('/feedback/<id>/delete')
def delete_feedback_post(id):
    """Delete a feedback post. Make sure only the author of the post can delete it"""

    # Get the post to be deleted
    feedback = Feedback.query.get_or_404(id)

    # Make sure a user is logged in
    if "username" not in session:
        flash('You must be logged in to do that!', 'danger')
        return redirect('/login')

    # Make sure the logged in user is the author of the post to be deleted
    elif session['username'] != feedback.user.username:

        # Delete the post
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.user.username}')
    
    else:
        flash('You are not authorized to do that!', 'danger')
        return redirect('/')







