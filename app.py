"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Rating

from utils import get_community_info, get_movie_for_comm, get_similar_movie

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Required to use Flask sessions and the debug toolbar
app.secret_key = "mysecret"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

# We have to set debug=True here, since it has to be True at the
# point that we invoke the DebugToolbarExtension
app.debug = False

connect_to_db(app)

# Use the DebugToolbar
DebugToolbarExtension(app)

@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<user_id>")
def show_user_page(user_id):
    """Show individual user's info"""

    user = User.query.get(user_id)
    ratings_list = db.session.query(Rating.score, Movie.title, Movie.imdb_url).join(Movie).filter(Rating.user_id==user_id).all()
    movie_id = Rating.query.filter_by(user_id=user.user_id).all()
    sim_movie=[]
    #print(movie_id[0])
    for i in movie_id:
        print(i.movie_id)
        sim_movie.append(get_similar_movie(i.movie_id))
    result=get_community_info()
    com_id=None
    if result[0].get(user_id) != None:
        com_id = result[0].get(user_id)
    return render_template("user_page.html", user=user, ratings_list=ratings_list,com_id=com_id, sim_movie=sim_movie)


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by('title').all()
    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie_page(movie_id):
    """Show individual movie's info"""

    movie = Movie.query.get(movie_id)
    user_id = session.get("user_id")
    if user_id:
        user_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()

    else:
        user_rating = None

    # Get average rating of movie
   
    avg_rating = 0

    prediction = None


    return render_template(
        "movie_page.html",
        movie=movie,
        user_rating=user_rating,
        average=avg_rating,
        prediction=prediction
        )


@app.route("/movies/<movie_id>", methods=["POST"])
def rate_movie_page(movie_id):
    """Show individual movie's info"""

    new_score = request.form.get("movie-rating")
    movie = Movie.query.get(movie_id)
    user_id=session["user_id"]

    rating = Rating.query.filter((Rating.user_id==user_id) & (Rating.movie_id==movie_id)).first()

    if not rating:
        rating = Rating(score=new_score, user_id=user_id, movie_id=movie_id)

    else:
        rating.score = new_score

    db.session.add(rating)
    db.session.commit()

    return redirect("/movies/%s" % movie_id)


@app.route("/login")
def show_login():
    """Shows the log-in form"""

    return render_template("login_form.html")



@app.route("/login", methods=["POST"])
def login_process():
    """Processes the login information"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Email does not exist. Please try again or register.")
        return redirect("/login")
    elif user and (user.password == password):
        flash("Login Successful.")
        session['user_id'] = user.user_id
        return redirect("/users/" + str(user.user_id))
    else:
        flash("Password incorrect. Please try again.")
        return redirect("/login")

@app.route("/logout")
def show_logout():
    """Shows the logout option"""

    flash("Logged out. Thanks for visiting Ratings!")
    del session['user_id']

    return redirect("/")

        

@app.route("/register")
def show_registration():
    """Shows the registration form"""

    return render_template("register_form.html")


    



@app.route("/communities",methods=["GET"])
def communities():
    """Shows Communities"""
    result=get_community_info()
    communities=result[1]
    new_communities=dict()
    for i,j in communities.items():
        l=get_movie_for_comm(i)
        if new_communities.get(i) == None:
            new_communities[i] = {'movies':l, 'members':j}
    return render_template("communities.html",communities=new_communities)

@app.route("/register", methods=["POST"])
def registration_process():
    """Processes the registration information"""

    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    if age:
        age = int(age)
    else:
        age=None
    zipcode = request.form.get("zipcode")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("You're already in our system. Please login.")
        return redirect("/login")
    else:
        #send info to update User database
        user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        #redirect to home
        flash("Registration Successful. Welcome to Ratings!")
        return redirect("/")


if __name__ == "__main__":
    app.run()
