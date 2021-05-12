import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
engine = create_engine('postgresql://postgres:asifnadish@localhost:5432/emo', echo=True)
db=scoped_session(sessionmaker(bind=engine))

f = open("songs_list.csv")
reader = csv.reader(f)

for song_title, song_url, singer, song_type in reader:
    db.execute("INSERT INTO Songs(song_title,song_url,singer,song_type)VALUES(:song_title,:song_url,:singer,:song_type)",{"song_title":song_title,"song_url":song_url,"singer":singer,"song_type":song_type})

db.commit()