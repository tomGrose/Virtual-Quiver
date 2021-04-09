from flask import current_app as app
import random
from models import db, connect_db, User, Disc, User_Wishlist, User_Disc, Manufacturer, Disc_Review, Rec_Disc, User_Broken_In_Disc, Review, Broken_In_Review
import numpy as np
from datetime import timedelta, datetime
from flask_mail import Mail, Message
from flask import url_for

def generate_ran_recs(users_discs):
    recs = []
    if len(users_discs) >=1:
        for disc in users_discs:
            similiar_discs = (Disc.query.filter_by(speed=f'{disc.speed}', 
                            high_stability=f'{disc.high_stability}', 
                            low_stability=f'{disc.low_stability}')
                            .filter(Disc.name != f"{disc.name}")
                            .all())
            for d in similiar_discs:
                new_rec_disc = Rec_Disc(id=d.id, 
                                        name=d.name, 
                                        plastic=d.plastic, 
                                        difficulty=d.difficulty, 
                                        speed=d.speed, 
                                        glide=d.glide, 
                                        high_stability=d.high_stability, 
                                        low_stability=d.low_stability, 
                                        image_url=d.image_url, 
                                        manufacturers_name=d.manufacturers_name, 
                                        disc_rec_based_on=disc.name)
                recs.append(new_rec_disc)
        
        random_discs = random.choices(recs, k = 30)
        return random_discs
    else:
        return []

    
def get_stats(users_discs):
    """Using numpi get the average stats of the discs in a users bag """

    discs_by_type = {'putters': [d for d in users_discs if d.disc_type == "putter"], 
                    'mids': [d for d in users_discs if d.disc_type == "mid"], 
                    'fairways': [d for d in users_discs if d.disc_type == "fairway"], 
                    'drivers': [d for d in users_discs if d.disc_type == "driver"] 
                    }


    discs_avgs = {'putters': {'total': 0, 'speed': 0, 'glide': 0, 'l_stability': 0, 'h_stability': 0}, 
                'mids': {'total': 0, 'speed': 0, 'glide': 0, 'l_stability': 0, 'h_stability': 0}, 
                'fairways': {'total': 0, 'speed': 0, 'glide': 0, 'l_stability': 0, 'h_stability': 0}, 
                'drivers': {'total': 0, 'speed': 0, 'glide': 0, 'l_stability': 0, 'h_stability': 0}, 
                }

    
    for disc_type, discs in discs_by_type.items():
        if len(discs) == 0:
            continue
        else:
            discs_avgs[disc_type]['total'] = len(discs_by_type[f'{disc_type}'])
            discs_avgs[disc_type]['speed'] = round(np.mean([d.speed for d in discs]), 1)
            discs_avgs[disc_type]['glide'] = round(np.mean([d.glide for d in discs]), 1)
            discs_avgs[disc_type]['l_stability'] = round(np.mean([d.low_stability for d in discs]), 1)
            discs_avgs[disc_type]['h_stability'] = round(np.mean([d.high_stability for d in discs]), 1)

    return discs_avgs



def populate_broken_in_discs(users_discs, users_broken_in_discs, current_user):
    """ Check on the timestamps from when a user added a disc to their quiver. If it is older than 4 months
    add that disc id and user id to the broken in discs model """

    broken_in_date = datetime.now() - timedelta(days = 120)
    broken_in_discs = User_Disc.query.filter(User_Disc.user_id == current_user.id, User_Disc.date_added <= broken_in_date).all()
    for d in broken_in_discs:
        disc = Disc.query.get(d.disc_id)
        if disc in users_broken_in_discs:
            continue
        else:
            broken_in_disc = User_Broken_In_Disc(user_id = current_user.id, disc_id = disc.id)
            db.session.add(broken_in_disc)
            db.session.commit()


def send_reset_email(mail, user):
    """ Send an email to a user with a time sensitive password reset token """
    token = user.get_pw_change_token()
    msg = Message('Password Reset Request', 
        sender='virtualquiverdiscs@gmail.com', 
        recipients=[user.email])
    
    msg.body = f'''To reset your password, please visit this link:
{url_for('reset_password', token=token, _external=True)}

If you did not make this request please ignore this email and no changes will be made to your account.
'''
    mail.send(msg)

def send_username_reminder(mail, user):
    """ Send a username reminder email to a user """

    msg = Message('Username Request', 
        sender='virtualquiverdiscs@gmail.com', 
        recipients=[user.email])
    
    msg.body = f'''Hello {user.first_name.capitalize()},

We have recieved a username reminder for the account associated with this email at virtualquiver.com.

Your username is {user.username}

If you did not make this request please ignore this email and no changes will be made to your account.
'''
    mail.send(msg)


# def clean_wish_discs(user, users_discs, user_wish_discs):
#     for d in user_wish_discs:
#         if d in users_discs:
#             wish_disc = User_Wishlist.query.filter_by(user_id = f'{user.id}', disc_id = f'{d.id}').first()
#             db.session.delete(wish_disc)
#             db.session.commit()