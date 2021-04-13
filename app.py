import os

from flask import Flask, render_template, request, flash, redirect, session, g, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy import func
from forms import (UserSignupForm, LoginForm, User_Discs_Recs, Disc_Search_Form, Delete_Account, User_Edit_Form, 
                User_Review, Forgot_Form, Reset_Password_Form, Change_Password_Form) 
from models import (db, connect_db, User, Disc, User_Wishlist, User_Disc, Manufacturer, 
                Disc_Review, Rec_Disc, User_Broken_In_Disc, Review, Broken_In_Review)
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, fresh_login_required
from datetime import timedelta, datetime
from flask_mail import Mail
from helpers import generate_ran_recs, get_stats, populate_broken_in_discs, send_reset_email, send_username_reminder


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///virtualQuiver'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secret")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'virtualquiverdiscs@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

toolbar = DebugToolbarExtension(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = 'You must login again before you make any changes'

mail = Mail(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            login_user(user, remember=True)
            populate_broken_in_discs(current_user.discs, current_user.broken_in_discs, current_user)
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
    """ Show a user's profile page """

    form = Delete_Account()
    return render_template('users/profile-settings.html', user=current_user, form=form)

        
@app.route('/users/delete', methods=['POST'])
@login_required
def delete_user_account():
    """ Delete a users account """
    should_delete = request.form.get('delete')

    if should_delete:
        user = User.query.get(current_user.id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash ("Account deleted succesfully", 'success')
        return redirect("/")
    flash('You did not select to have your account deleted', 'danger')
    return redirect(url_for('show_user_profile', user_id=current_user.id))


@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@fresh_login_required
def edit_users_account(user_id):
    """ Allow a user to update their account info """

    if user_id != current_user.id:
        flash("You do not have permission to do that", "danger")
        return redirect("/")

    form = User_Edit_Form(obj=current_user)

    if form.validate_on_submit():
        user = current_user
        try:
            user.username = form.username.data
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.location = form.location.data
            user.image_url = form.image_url.data

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            flash("Username already taken", 'danger')
            return render_template('users/sign-up.html', form=form)

        flash("Information updated!", "success")
        return redirect(url_for('show_user_profile', user_id=current_user.id))

    return render_template('users/user-edit-form.html', form=form)


@app.route('/users/forgot-password', methods=["GET", "POST"])
def forgot_password_request():
    """Show form for a user to be able to request a reset password email"""

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = Forgot_Password_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(mail, user)
        flash('An email has been sent with instructions to reset your password', 'success')
        return redirect(url_for('homepage'))

    return render_template('users/forgot-password.html', form=form)


@app.route('/users/forgot-username', methods=["GET", "POST"])
def forgot_username():
    """Show form for a user to be able to request a reset password email"""

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    form = Forgot_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_username_reminder(mail, user)
        flash('An email has been sent with your username', 'success')
        return redirect(url_for('homepage'))

    return render_template('users/forgot-username.html', form=form)


@app.route('/users/password-reset/<token>', methods=["GET", "POST"])
def reset_password(token):
    """ Provide the user with a page to reset their password if their token is authentic """

    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    user = User.verify_token(token)

    if user is None:
        flash('That is an expired or invalids token', 'danger')
        return redirect(url_for('forgot_password_request'))
    
    form = Reset_Password_Form()
    if form.validate_on_submit():
        new_password = form.password.data
        user.change_password(new_password)
        db.session.commit()
        flash('Your password has been updated, you are now able to login', 'success')
        return redirect(url_for('login'))

    return render_template('users/reset-password.html', form=form)


@app.route('/users/password-change/<int:user_id>', methods=["GET", "POST"])
@fresh_login_required
def change_password(user_id):
    """ Provide the user with a page to change their password when already logged in """

    if user_id != current_user.id:
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('homepage'))

    form = Change_Password_Form()
    if form.validate_on_submit():
        current_password = form.current_password.data
        if User.authenticate(current_user.username, current_password):
            new_password = form.password.data
            current_user.change_password(new_password)
            db.session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('login'))
        else:
            form.current_password.errors.append('Password Incorrect!')
    return render_template('users/reset-password.html', form=form)
        

    

# ##############################################################################
# # Disc routes:

@app.route('/discs/discover/page/<int:page_num>', methods=['GET', 'POST'])
def show_discs(page_num):
    """ Show all the discs in the database, allow users to search for discs using filters. If a user is
    logged in they will be able to add the discs to their bag, or wishlist """

    discs = (Disc.query.paginate(per_page=21, page=page_num, error_out=True))
    user_discs = []
    user_wishes = []

    form = Disc_Search_Form()

    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        user_discs = user.discs
        user_wishes = user.wish_discs

    

    if form.validate_on_submit():

        filters = {}

        if form.difficulty_check.data:
            filters['difficulty'] = form.difficulty.data
            
        if form.speed_check.data:
            filters['speed'] = form.speed.data

        if form.glide_check.data:
            filters['glide'] = form.glide.data

        if form.h_stability_check.data:
            filters['high_stability'] = form.high_stability.data

        if form.l_stability_check.data:
            filters['low_stability'] = form.low_stability.data

        if form.disc_type.data != 'all':
            filters['disc_type'] = form.disc_type.data
         

        search_discs = (Disc.query.filter_by(**filters)
                                            .paginate(per_page=21, page=page_num, error_out=True))

    
        return render_template('discs/discover-discs.html', 
                            threads=search_discs, 
                            users_discs=user_discs, 
                            user_wishes=user_wishes,
                            form=form)

    return render_template('discs/discover-discs.html', 
                            threads=discs, 
                            users_discs=user_discs, 
                            user_wishes=user_wishes,
                            form=form)


@app.route('/discs/add', methods=['POST'])
@login_required
def add_users_disc():
    """ Route to dynamically add a disc to a user's bag by calling it with javascript """

    disc_id = request.json.get('disc_id')
    disc = Disc.query.get_or_404(disc_id)

    if disc in current_user.wish_discs:
        wish_disc = User_Wishlist.query.filter_by(user_id = f'{current_user.id}', disc_id = f'{disc.id}').first()
        db.session.delete(wish_disc)
        db.session.commit()

    users_new_disc = User_Disc(user_id=current_user.id, disc_id=disc.id)
    db.session.add(users_new_disc)
    db.session.commit()

    resp = jsonify({"disc_added": "Success"})
    return (resp, 201)


@app.route('/discs/remove', methods=['POST'])
@login_required
def remove_users_disc():
    """ Route to dynamically remove a disc to a user's bag by calling it with javascript """

    disc_id = request.json.get('disc_id')
    users_disc = User_Disc.query.filter(User_Disc.user_id == current_user.id, User_Disc.disc_id == disc_id).first()
    db.session.delete(users_disc)
    db.session.commit()
    resp = jsonify({"disc_removed": "Success"})
    return (resp, 201)


@app.route('/discs/wishlist/add', methods=['POST'])
@login_required
def add_users_wish():
    """ Route to dynamically add a disc to a user's wishlist by calling it with javascript """

    disc_id = request.json.get('disc_id')
    disc = Disc.query.get_or_404(disc_id)
    users_new_wish = User_Wishlist(user_id=current_user.id, disc_id=disc.id)
    db.session.add(users_new_wish)
    db.session.commit()
    resp = jsonify({"disc_added_to_wishlist": "Success"})
    return (resp, 201)

@app.route('/discs/wishlist/remove', methods=['POST'])
@login_required
def remove_from_wishlist():
    """ Provide a post route for discs to be dynamically removed from a users wishlist """

    disc_id = request.json.get('disc_id')
    wish = User_Wishlist.query.filter(User_Wishlist.user_id == current_user.id, User_Wishlist.disc_id == disc_id).first()
    db.session.delete(wish)
    db.session.commit()
    resp = jsonify({'disc_removed_from_wishlist': 'Success'})
    return (resp, 201)

@app.route('/discs/search')
def search_discs():
    """ View to handle users searching for discs with the search bar """

    disc_name = request.args.get('disc_name')
    discs = (Disc.query.filter(Disc.name.like(f"%{disc_name}%")).paginate(per_page=21, page=1, error_out=True))
    user_discs = []
    user_wishes = []
    form = Disc_Search_Form()

    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        user_discs = user.discs
        user_wishes = user.wish_discs

    return render_template('discs/discover-discs.html', threads=discs, users_discs=user_discs, user_wishes=user_wishes, form=form)


@app.route('/discs/recommendations/disc/<int:disc_id>/page/<int:page_num>', methods=['GET', 'POST'])
@login_required
def show_similiar_discs(disc_id, page_num):
    """ Show a user similiar discs to one they selected """

    form = User_Discs_Recs()
    disc = Disc.query.get_or_404(disc_id)
    if form.validate_on_submit():
        disc = form.options.data

    similiar_discs_threads = (Disc.query.filter_by(speed=f'{disc.speed}', 
                        high_stability=f'{disc.high_stability}', 
                        low_stability=f'{disc.low_stability}')
                        .filter(Disc.name != f"{disc.name}")
                        .paginate(per_page=21, page=page_num, error_out=True))

    return render_template('discs/disc-recommendations.html', disc=disc, threads=similiar_discs_threads, form=form)


@app.route('/discs/recommendations', methods=['GET', 'POST'])
@login_required
def show_users_recommendations():
    """ Show a random assortment of recommendations based on the discs the user has in their bag
    Allow the user to search for reccomendations based specifically on one disc"""

    users_discs = current_user.discs
    rec_discs = generate_ran_recs(users_discs)
    form = User_Discs_Recs()
    if form.validate_on_submit():
        page_num = 1
        disc = form.options.data
        similiar_discs_threads = (Disc.query.filter_by(speed=f'{disc.speed}', 
                        high_stability=f'{disc.high_stability}', 
                        low_stability=f'{disc.low_stability}')
                        .filter(Disc.name != f"{disc.name}")
                        .paginate(per_page=21, page=page_num, error_out=True))

        return render_template('discs/disc-recommendations.html', disc=disc, threads=similiar_discs_threads, form=form)
    return render_template('discs/users-recommendations.html', discs=rec_discs, form=form)


@app.route('/discs/wishlist')
@login_required
def show_wishlist():
    """Show the discs currently in a users wishlist"""

    discs = current_user.wish_discs
    return render_template('discs/wish-discs.html', discs=discs)


@app.route('/discs/<int:disc_id>', methods=['POST', 'GET'])
def show_disc_page(disc_id):
    """ Show more information for a particular disc, including reviews"""

    form = User_Review()
    disc = Disc.query.get_or_404(disc_id)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        throw_type = form.throw_type.data
        review = Review(user_id=current_user.id, 
                    username=current_user.username, 
                    disc_id=disc.id, 
                    title=title, 
                    throw_type=throw_type, 
                    content=content)

        db.session.add(review)
        db.session.commit()
        flash("Review Added!", "success")
        return redirect(url_for('show_disc_page', disc_id=disc.id))
    
    users_discs = current_user.discs
    users_wish_discs = current_user.wish_discs
    disc_in_bag_count = User_Disc.query.filter_by(disc_id = f'{disc.id}').count()
    disc_in_wish_count = User_Wishlist.query.filter_by(disc_id = f'{disc.id}').count()
    reviews = Review.query.filter_by(disc_id=f'{disc.id}').all()
    broken_in_reviews = Broken_In_Review.query.filter_by(disc_id=f'{disc.id}').all()
    return render_template('discs/disc.html', 
                            disc=disc, 
                            reviews=reviews, 
                            broken_in_reviews=broken_in_reviews, 
                            form=form, 
                            disc_count=disc_in_bag_count, 
                            wish_count=disc_in_wish_count,
                            users_discs = users_discs,
                            users_wish_discs = users_wish_discs)


@app.route('/discs/review/<int:disc_id>', methods=['POST', 'GET'])
@login_required
def leave_broken_in_review(disc_id):
    """ A review page for a user who has had a disc in their bag for more than 4 months to leave a review """

    disc = Disc.query.get_or_404(disc_id)
    if disc not in current_user.broken_in_discs:
        flash("You do not have permission to leave a broken in review for this disc yet.", "danger")
        return redirect('/')

    form = User_Review()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        review = Broken_In_Review(user_id=current_user.id, username=current_user.username, disc_id=disc.id, title=title, content=content)
        db.session.add(review)
        db.session.commit()
        flash("Review Added!", "success")
        return redirect('/')
    
    return render_template('discs/disc-broken-in-review.html', form=form)


# ##############################################################################
# # Homepage and error pages


@app.route('/')
def homepage():
    """Show landing page where users can sign up or log in"""

    if current_user.is_authenticated:
        users_discs = current_user.discs
        user_wishlist = current_user.wish_discs
        bag_stats = get_stats(users_discs)
        broken_in_discs = current_user.broken_in_discs
        return render_template('home.html', 
                            user=current_user, 
                            users_discs=users_discs, 
                            user_wishlist=user_wishlist, 
                            bag_stats=bag_stats, 
                            broken_in_discs=broken_in_discs)
    else:
        return render_template('landing.html')


# ##############################################################################
# # Informational pages

@app.route('/about')
def show_about():
    """ SHow about page for the website"""
    return render_template('about.html')


@app.route('/information')
def show_info():
    return render_template('info.html')
