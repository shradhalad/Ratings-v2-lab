"""Server for movie ratings app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def allmovies():
    """View a list of all movies"""

    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)


@app.route('/users')
def allusers():
    """View a list of all users"""

    users = crud.get_all_users()
    return render_template("all_users.html", users=users)

@app.route('/users/<user_id>')
def show_user_profile(user_id):
    """Shows profile of a particular user"""

    user = crud.get_user_by_id(user_id)
    return render_template("user_profile.html", user=user)

#have issues with this one - it lets you register without entering a password
@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user & checks if the email has been used before."""
    
    email = request.form.get("email")
    password = request.form.get("password")

    # print(type(password))

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    if len(password) <= 7:
        flash("Password length must be at least 8 characters long. Try again.")
    else:
        crud.create_user(email, password)
        flash("Account created! Please log in.")
        return redirect(f"users/<{user.id}>")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """Lets the user login & checks if the inputs match or not"""
    #make sure that the email we get matches an existing email
    #make sure password matches the password of that email account
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    stored_password = crud.get_user_password(email)

    if not user:
        flash("Incorrect email entered! Try again.")
    elif password != stored_password:
        flash("Incorrect password entered! Try again.")
    elif not user and password != stored_password:
        flash("Incorrect email and/or password entered! Try again.")
    else:
        session["user_email"] = email
        flash("You have logged in successfully!")
        return redirect("/movies")
        #store as cookies
        # set cookie variable = to user
        #user_email = email
        
    return redirect("/")

# Allow Users to Rate Movies
# Users who have successfully logged into the web app should be able to rate a movie from 0–5.
# on each movie details page (in the html) there should be a form asking for a rating
# form would check if user is in session
# user profile html would show the ratings the user has created
# movie detail html would show the rating the user has created
#further further studies = make limit so user can only rate a specific movie once 

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
