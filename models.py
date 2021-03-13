"""SQLAlchemy models for Virtual Quiver"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(UserMixin, db.Model):
    """User model for Virtual Quiver"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    location = db.Column(
        db.Text
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    discs = db.relationship(
        'Disc', secondary="users_discs", backref="user")

    wish_discs = db.relationship(
        'Disc', secondary="wishlists", backref="user_wish")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def change_password(self, new_password):
        """ Allow a user to create a new password and store it"""

        hashed_pwd = bcrypt.generate_password_hash(new_password).decode('UTF-8')

        self.password = hashed_pwd

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

    image_url = db.Column(
        db.Text,
        default="",
    )
    manufacturers_name = db.Column(
        db.Text,
        db.ForeignKey('manufacturers.name')
    )

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

class Review(db.Model):
    """List of manufacturers"""

    __tablename__ = 'reviews'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade")
    )

    username = db.Column(
        db.Text,
        db.ForeignKey('users.username', ondelete="cascade")
    )

    disc_id = db.Column(
        db.Integer,
        db.ForeignKey('discs.id', ondelete="cascade")
    )

    content = db.Column(
        db.Text,
        nullable=False
    )


