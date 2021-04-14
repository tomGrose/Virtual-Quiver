from flask_login import LoginManager, current_user
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo, ValidationError
from wtforms.widgets import TextArea
from wtforms_alchemy.fields import QuerySelectField
from models import Disc, User, Innapropriate_Word, US_STATES

BaseModelForm = model_form_factory(FlaskForm)

### HELPER FUNCTIONS ###

def choice_query():
    return current_user.discs

### Validator Functions ###

def check_vulgar_words(form, field):
        content = field.data
        for w in Innapropriate_Word.query.all():
            if w.word in content:
                raise ValidationError(f'{w.word} is not allowed')

class UserSignupForm(BaseModelForm):
    """Form for adding users."""

    class Meta:
        model = User
        exclude = ['alternate_id']

    def validate_username(self, username):
        username = username.data
        if " " in username:
            raise ValidationError('No spaces in usernames')
        else:
            for w in Innapropriate_Word.query.all():
                if w.word in username:
                    raise ValidationError(f'{w.word} is not allowed')

    def validate_password(self, password):
        pw = password.data
        if " " in pw:
            raise ValidationError('No spaces in passwords')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class User_Discs_Recs(BaseModelForm):
    """Form for a user to see recommendations for discs based on the ones they own"""

    options = QuerySelectField('Disc', query_factory=choice_query, allow_blank=False, get_label='name')


class Disc_Search_Form(FlaskForm):
    """Form for editing users."""

    difficulty_check = BooleanField('Search Difficulty')
    difficulty = IntegerRangeField('Difficulty', id="difficultyId")
    speed_check = BooleanField('Search Speed')
    speed = IntegerRangeField('Speed', id="speedId")
    glide_check = BooleanField('Search Glide')
    glide = IntegerRangeField('Glide', id="glideId")
    l_stability_check = BooleanField('Search Fade')
    low_stability = IntegerRangeField('Low Stability', id="low_stabilityId")
    h_stability_check = BooleanField('Search Turn')
    high_stability = IntegerRangeField('High Stability', id="high_stabilityId")
    disc_type = SelectField('Disc Type', 
                            choices=[
                            ('all', 'All Discs'), 
                            ('putter', 'Putter'), 
                            ('mid', 'Mid Range'), 
                            ('fairway', 'Fairway Driver'), 
                            ('driver', 'Driver')]
                            )


class Delete_Account(FlaskForm):
    delete = BooleanField('Yes, delete my account.')


class User_Edit_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), check_vulgar_words])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    location = SelectField('State', validators=[DataRequired()], choices=US_STATES)
    image_url = StringField('(Optional) Profile Image URL')


class User_Review(FlaskForm):
    title = StringField('Review Title', validators=[DataRequired(), Length(max=60), check_vulgar_words])
    throw_type = SelectField('Throw Type', 
                            choices=[
                            ('backhand', 'Backhand'), 
                            ('forehand', 'Forehand')],
                            validators=[DataRequired()]
                            )
    content = StringField('Review Content', widget=TextArea(), validators=[DataRequired(), check_vulgar_words])
    
class Forgot_Form(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email')

class Reset_Password_Form(FlaskForm):
    password = PasswordField("New Password", validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField("Verify Password", validators=[Length(min=6), DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class Change_Password_Form(FlaskForm):
    current_password = PasswordField("Verify Current Password", validators=[Length(min=6), DataRequired()])
    password = PasswordField("New Password", validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField("Verify Password", validators=[Length(min=6), DataRequired(), EqualTo('password')])


