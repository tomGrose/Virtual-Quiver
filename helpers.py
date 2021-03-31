import app
import random
from models import db, connect_db, User, Disc, User_Wishlist, User_Disc, Manufacturer, Disc_Review, Rec_Disc, User_Broken_In_Disc, Review, Broken_In_Review
import numpy as np
from datetime import timedelta, datetime


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
            discs_avgs[disc_type]['total'] += 1
            discs_avgs[disc_type]['speed'] = round(np.mean([d.speed for d in discs]), 1)
            discs_avgs[disc_type]['glide'] = round(np.mean([d.glide for d in discs]), 1)
            discs_avgs[disc_type]['l_stability'] = round(np.mean([d.low_stability for d in discs]), 1)
            discs_avgs[disc_type]['h_stability'] = round(np.mean([d.high_stability for d in discs]), 1)

    return discs_avgs



def populate_broken_in_discs(users_discs, users_broken_in_discs, current_user):
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





# US_STATES = [
#     (u'alabama', u'AL'),
#     (u'alaska', u'AK'),
#     (u'arizona', u'AZ'),
#     (u'arkansas', u'AR'),
#     (u'california', u'CA'),
#     (u'colorado', u'CO'),
#     (u'connecticut', u'CT'),
#     (u'deleware', u'DE'),
#     (u'florida', u'FL'),
#     (u'georgia', u'GA'),
#     (u'hawaii', u'HI'),
#     (u'idaho', u'ID'),
#     (u'illinois', u'IL'),
#     (u'indiana', u'IN'),
#     (u'iowa', u'IA'),
#     (u'kansas', u'KS'),
#     (u'kentucky', u'KY'),
#     (u'louisiana', u'LA'),
#     (u'maine', u'ME'),
#     (u'maryland', u'MD'),
#     (u'massachusetts', u'MA'),
#     (u'michigan', u'MI'),
#     (u'minnesota', u'MN'),
#     (u'mississippi', u'MS'),
#     (u'missouri', u'MO'),
#     (u'montana', u'MT'),
#     (u'nebraska', u'NE'),
#     (u'nevada', u'NV'),
#     (u'new hampshire', u'NH'),
#     (u'new jersey', u'NJ'),
#     (u'new mexico', u'NM'),
#     (u'new york', u'NY'),
#     (u'north carolina', u'NC'),
#     (u'north dakota', u'ND'),
#     (u'ohio', u'OH'),
#     (u'oklahoma', u'OK'),
#     (u'oregon', u'OR'),
#     (u'pennsylvania', u'PA'),
#     (u'rhode island', u'RI'),
#     (u'south carolina', u'SC'),
#     (u'south dakota', u'SD'),
#     (u'tennessee', u'TN'),
#     (u'texas', u'TX'),
#     (u'utah', u'UT'),
#     (u'vermont', u'VT'),
#     (u'virginia', u'VA'),
#     (u'washington', u'WA'),
#     (u'west virginia', u'WV'),
#     (u'wisconsin', u'WI'),
#     (u'wyoming', u'WY')
#     ]