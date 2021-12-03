"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


# Functions start here!
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    db.session.add(movie)
    db.session.commit()

    return movie

def get_movies():
    """Return all movies."""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Takes in movie id & returns the movie linked to it"""

    return Movie.query.get(movie_id)

def get_all_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Takes in user id & returns the user linked to it"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Takes in user email & returns the user linked to it 
    if it exists, else it returns None"""

    return User.query.filter(User.email==email).first()

def get_user_password(email):
    """Takes in an existing user & returns the password linked to it"""
    current_user = get_user_by_email(email)

    return current_user.password


def create_rating(user, movie, score):
    """Create and return a new rating."""
    rating = Rating(user=user, movie=movie, score=score)

    db.session.add(rating)
    db.session.commit()

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)