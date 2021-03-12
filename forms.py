from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email



class UserSignupForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    location = StringField('State', validators=[DataRequired()])
    image_url = StringField('(Optional) Profile Image URL')
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


# class DiscSearchForm(FlaskForm):
#     """Form for editing users."""

#     difficulty = StringField('Username', validators=[DataRequired()])
#     speed = StringField('E-mail', validators=[DataRequired(), Email()])
#     glide = StringField('(Optional)')
#     low_stability = StringField('(Optional) Header Image URL')
#     high_stability = TextAreaField('(Optional) Bio')
#     disc_type = 

# class ChangePasswordForm(FlaskForm):
#     password = PasswordField("Current password", validators=[Length(min=6)])
#     new_password = PasswordField("New Password", validators=[Length(min=6)])
#     new_password_check = PasswordField("Re-type new Password", validators=[Length(min=6)])
