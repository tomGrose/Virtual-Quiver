## Import data about manufacturers and discs from the API and save them the database ##

import requests
from models import db, connect_db, Disc, Manufacturer, Innapropriate_Word
from app import db



def populate_manufacturers():
    """ Populate the manufacturers for the discs using the API"""
    resp = requests.get(
                "https://disc-golf-collection.herokuapp.com/api/companies")


    data = resp.json()

    companies = data.get('Companies')

    for c in companies:
        new_manufact = Manufacturer(name=c.get('name'))
        db.session.add(new_manufact)



def populate_discs():
    """ Populate all the discs from the API"""
    resp = requests.get(
                "https://disc-golf-collection.herokuapp.com/api/discs")

    data = resp.json()


    discs = data.get("discs")


    for disc in discs:
        disc_type = ''
        name = disc.get('name')
        plastic = disc.get('plastic')
        diff = disc.get('difficulty')
        speed = disc.get('speed')
        glide = disc.get('glide')
        h_stability = disc.get('high_stability')
        l_stability = disc.get('low_stability')
        manufacturer = disc.get('compaby_name')
        image_url = disc.get('image_url')
        speed_int = int(speed)
        if speed_int <= 3:
            disc_type = 'putter'
        if speed_int > 3 and speed <= 5:
            disc_type = 'mid'
        if speed_int > 5 and speed <= 8:
            disc_type = 'fairway'
        if speed_int > 8:
            disc_type = 'driver'

        
        new_disc = Disc(name=name, plastic=plastic, difficulty=diff, speed=speed, glide=glide, 
                        high_stability=h_stability, low_stability=l_stability, disc_type = disc_type, 
                        image_url=image_url, manufacturers_name=manufacturer)
        db.session.add(new_disc)
       

def populate_innapropriate_words(): 
    file = open("static/text/vulgar-words.txt", "r")


    for w in file:
        stripped_word = str(w.strip("\n"))
        new_word = Innapropriate_Word(word=stripped_word)
        db.session.add(new_word)


    file.close()

db.drop_all()
db.create_all()

populate_manufacturers()
db.session.commit()
populate_discs()
db.session.commit()
populate_innapropriate_words()
db.session.commit()
