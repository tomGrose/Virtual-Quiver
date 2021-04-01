"""SQLAlchemy models for Virtual Quiver"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType, URLType, ChoiceType
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
from furl import furl
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(UserMixin, db.Model):
    """User model for Virtual Quiver"""

    __tablename__ = 'users'

    TYPES = [
    (u'alabama', u'AL'),
    (u'alaska', u'AK'),
    (u'arizona', u'AZ'),
    (u'arkansas', u'AR'),
    (u'california', u'CA'),
    (u'colorado', u'CO'),
    (u'connecticut', u'CT'),
    (u'deleware', u'DE'),
    (u'florida', u'FL'),
    (u'georgia', u'GA'),
    (u'hawaii', u'HI'),
    (u'idaho', u'ID'),
    (u'illinois', u'IL'),
    (u'indiana', u'IN'),
    (u'iowa', u'IA'),
    (u'kansas', u'KS'),
    (u'kentucky', u'KY'),
    (u'louisiana', u'LA'),
    (u'maine', u'ME'),
    (u'maryland', u'MD'),
    (u'massachusetts', u'MA'),
    (u'michigan', u'MI'),
    (u'minnesota', u'MN'),
    (u'mississippi', u'MS'),
    (u'missouri', u'MO'),
    (u'montana', u'MT'),
    (u'nebraska', u'NE'),
    (u'nevada', u'NV'),
    (u'new hampshire', u'NH'),
    (u'new jersey', u'NJ'),
    (u'new mexico', u'NM'),
    (u'new york', u'NY'),
    (u'north carolina', u'NC'),
    (u'north dakota', u'ND'),
    (u'ohio', u'OH'),
    (u'oklahoma', u'OK'),
    (u'oregon', u'OR'),
    (u'pennsylvania', u'PA'),
    (u'rhode island', u'RI'),
    (u'south carolina', u'SC'),
    (u'south dakota', u'SD'),
    (u'tennessee', u'TN'),
    (u'texas', u'TX'),
    (u'utah', u'UT'),
    (u'vermont', u'VT'),
    (u'virginia', u'VA'),
    (u'washington', u'WA'),
    (u'west virginia', u'WV'),
    (u'wisconsin', u'WI'),
    (u'wyoming', u'WY')
    ]

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    alternate_id = db.Column(
        db.Integer
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True,
        info={'label': 'Username'}
    )

    email = db.Column(
        EmailType,
        nullable=False,
        unique=True,
        info={'label': 'Email'}
    )

    first_name = db.Column(
        db.String,
        nullable=False,
        info={'label': 'First Name'}
    )

    last_name = db.Column(
        db.String,
        nullable=False,
        info={'label': 'Last Name'}
    )

    image_url = db.Column(
        URLType, 
        default='https://thumbs.dreamstime.com/z/disc-golf-frisbee-vector-eps-hand-drawn-crafteroks-svg-free-file-dxf-logo-silhouette-icon-instant-download-digital-cutting-clipart-146467312.jpg', 
        info={'label': '(optional) Profile Image URL'}
    )

    location = db.Column(
        ChoiceType(TYPES)
    )

    password = db.Column(
        db.String,
        nullable=False,
    )

    discs = db.relationship(
        'Disc', secondary="users_discs", backref="user")

    wish_discs = db.relationship(
        'Disc', secondary="wishlists", backref="user_wish")

    broken_in_discs = db.relationship(
        'Disc', secondary="broken_in_discs")


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    def change_password(self, new_password):
        """ Allow a user to create a new password and store it"""

        hashed_pwd = bcrypt.generate_password_hash(new_password).decode('UTF-8')

        self.password = hashed_pwd

    def get_pw_change_token(self, expires_sec=1800):
        """ Create a timed sensitive token for a user to be able to reset password"""

        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    def change_pw(self, new_password):
        """ Hash a users new password from their password reset and adds it to their model """

        hashed_pwd = bcrypt.generate_password_hash(new_password).decode('UTF-8')

        self.password = hashed_pw
        


    @classmethod
    def verify_token(cls, token):
        """ Verify reset token is valid """

        s = Serializer(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

  
    @classmethod
    def signup(cls, username, email, first_name, last_name, image_url, location, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
            location=location,
            password=hashed_pwd

        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            user_is_auth = bcrypt.check_password_hash(user.password, password)
            if user_is_auth:
                return user

        return False

class Manufacturer(db.Model):
    """Model for a manufacturer of discs"""

    __tablename__ = 'manufacturers'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

class Disc(db.Model):
    """Model for a disc golf disc"""

    __tablename__ = 'discs' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False
    )

    plastic = db.Column(
        db.Text
    )

    difficulty = db.Column(
        db.Float,
        default=0
    )

    speed = db.Column(
        db.Float,
        nullable=False
    )

    glide = db.Column(
        db.Float,
        nullable=False
    )

    high_stability = db.Column(
        db.Float,
        nullable=False
    )

    low_stability = db.Column(
        db.Float,
        nullable=False
    )

    disc_type = db.Column(
        db.Text,
    )

    image_url = db.Column(
        db.Text,
        default="",
    )
    manufacturers_name = db.Column(
        db.Text,
        db.ForeignKey('manufacturers.name')
    )

    def __repr__(self):
        return f"ID: {self.id} Name: {self.name}"


class User_Wishlist(db.Model):
    """Model for holding a users id and disc id for their wishlist"""

    __tablename__ = 'wishlists' 


    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    disc_id = db.Column(
        db.Integer,
        db.ForeignKey('discs.id', ondelete="cascade")
    )


class User_Disc(db.Model):
    """Model for holding the discs a user has in their bag by matching their id to the disc id"""

    __tablename__ = 'users_discs' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    disc_id = db.Column(
        db.Integer,
        db.ForeignKey('discs.id', ondelete="cascade")
    )

    date_added = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

class User_Broken_In_Disc(db.Model):
    """ Table Containing relationship from a user to discs 
    if they have been in the users bag for over four months """

    __tablename__ = 'broken_in_discs'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    disc_id = db.Column(
        db.Integer,
        db.ForeignKey('discs.id', ondelete="cascade")
    )

class Disc_Review(db.Model):
    """Abstract table for regular reviews and broken in reviews to inherit from """

    __abstract__ = True

    TYPES = {'backhand':'Backhand', 'forehand':'Forehand'}

    @declared_attr
    def user_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('users.id', ondelete="cascade")
            )

    @declared_attr
    def username(cls):
        return db.Column(
            db.Text,
            db.ForeignKey('users.username', ondelete="cascade")
            )

    @declared_attr
    def disc_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey('discs.id', ondelete="cascade")
            )


    title = db.Column(
        db.Text,
        nullable=False
    )

    throw_type = db.Column(
        ChoiceType(TYPES),
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

class Review(Disc_Review):
    """ Model for holding the reviews users have left for discs """
    
    __tablename__ = 'reviews'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

class Broken_In_Review(Disc_Review):

    __tablename__ = 'broken_in_reviews'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

class Rec_Disc(Disc, db.Model):
    __abstract__ = True

    id = db.Column(db.Integer)
    disc_rec_based_on = db.Column(db.Text)
