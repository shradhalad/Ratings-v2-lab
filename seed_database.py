''' Automates all database functions.'''

import os
import json
from random import randint, choice
from datetime import datetime
import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
#open -> opens a stream & set it as f
#.read reads the stream & .loads turns it from array or object into a list or dict (correspondingly)
#movie_data is a list (check movies.json in the data folder to see that the [] makes it a array)

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = (movie["title"], movie["overview"], movie["poster_path"],)

    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    #ignore the blue highlighted %d, it's VS code being weird

    #make movie with function from crud, then append it to movies_in_db
    new_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(new_movie)


for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email, password)

    for x in range(10):
        random_movie = choice(movies_in_db)
        random_score = randint(1, 5)

        crud.create_rating(user, random_movie, random_score)



