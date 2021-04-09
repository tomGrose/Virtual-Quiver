from models import db, connect_db, Innapropriate_Word
from app import db

file = open("static/text/vulgar-words.txt", "r")

words = []

for w in file:
    stripped_word = str(w.strip("\n"))
    new_word = Innapropriate_Word(word=stripped_word)
    db.session.add(new_word)

db.session.commit()

file.close()