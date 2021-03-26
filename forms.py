from flask_login import LoginManager, current_user
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.fields.html5 import DecimalRangeField, IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from wtforms_alchemy.fields import QuerySelectField
from models import Disc, User

BaseModelForm = model_form_factory(FlaskForm)

def choice_query():
    return current_user.discs

class UserSignupForm(BaseModelForm):
    """Form for adding users."""

    class Meta:
        model = User
        exclude = ['alternate_id']
    # username = StringField('Username', validators=[DataRequired()])
    # email = StringField('E-mail', validators=[DataRequired(), Email()])
    # first_name = StringField('First Name', validators=[DataRequired()])
    # last_name = StringField('Last Name', validators=[DataRequired()])
    # location = StringField('State', validators=[DataRequired()])
    # image_url = StringField('(Optional) Profile Image URL')
    # password = PasswordField('Password', validators=[Length(min=6)])


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
    l_stability_check = BooleanField('Search Low Stability')
    low_stability = IntegerRangeField('Low Stability', id="low_stabilityId")
    h_stability_check = BooleanField('Search High Stability')
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
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    location = StringField('State', validators=[DataRequired()])
    image_url = StringField('(Optional) Profile Image URL')

# class Search_Similiar_Disc(FlaskForm):
#     more_speed =

# class ChangePasswordForm(FlaskForm):
#     password = PasswordField("Current password", validators=[Length(min=6)])
#     new_password = PasswordField("New Password", validators=[Length(min=6)])
#     new_password_check = PasswordField("Re-type new Password", validators=[Length(min=6)])
