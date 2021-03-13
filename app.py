import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from forms import UserSignupForm, LoginForm
from models import db, connect_db, User, Disc, User_Wishlist, User_Disc, Manufacturer, Review
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

CURR_USER = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///virtualQuiver'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "SupaSecret")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.init_app(app)

connect_db(app)
db.create_all()


##############################################################################
# User signup/login/logout


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def add_user_to_global():
    """If a user is logged in add them to the global variable"""

    if current_user.is_authenticated:
        g.user = User.query.get(current_user.id)

    else:
        g.user = None



@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Handle user signup.
    Create new user and add to DB. Redirect to the user's logged in home page.

    """

    form = UserSignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                location=form.location.data,
                password=form.password.data

            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/sign-up.html', form=form)

        login_user(user)

        return redirect("/")

    else:
        return render_template('users/sign-up.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            login_user(user)
            flash("Welcome Back!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Handle logout of user."""

    logout_user()
    flash ("Logged out succesfully!", 'success')
    return redirect("/")


##############################################################################
# General user routes:

@app.route('/users/profile/<int:user_id>')
@login_required
def show_user_profile(user_id):


    return render_template('users/profile-settings.html', user=current_user)
        


# ##############################################################################
# # Disc routes:

@app.route('/discs/discover')
def show_discs():

    discs = (Disc.query.limit(50).all())
    user_discs = []
    user_wishes = []

    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        user_discs = user.discs
        user_wishes = user.wish_discs

    return render_template('discs/discover-discs.html', discs=discs, users_discs=user_discs, user_wishes=user_wishes)


@app.route('/discs/add', methods=['POST'])
def add_users_disc():
    disc_id = request.json.get('disc_id')
    disc = Disc.query.get_or_404(disc_id)
    users_new_disc = User_Disc(user_id=current_user.id, disc_id=disc.id)
    db.session.add(users_new_disc)
    db.session.commit()
    resp = jsonify({"disc_added": "Success"})
    return (resp, 201)


@app.route('/discs/wishlist/add', methods=['POST'])
def add_users_wish():
    disc_id = request.json.get('disc_id')
    disc = Disc.query.get_or_404(disc_id)
    users_new_wish = User_Wishlist(user_id=current_user.id, disc_id=disc.id)
    db.session.add(users_new_wish)
    db.session.commit()
    resp = jsonify({"disc_added_to_wishlist": "Success"})
    return (resp, 201)




# ##############################################################################
# # Homepage and error pages


@app.route('/')
def homepage():
    """Show landing page where users can sign up or log in"""

    if current_user.is_authenticated:
        users_discs = current_user.discs
        return render_template('home.html', user=current_user, users_discs=users_discs)
    else:
        return render_template('landing.html')


# ##############################################################################
# # Turn off all caching in Flask
# #
# # https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
