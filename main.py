from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
# Import FloatField for numeric input and NumberRange for validation
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
import requests

# --- API Configuration ---
# You need to get your own API key from themoviedb.org
MOVIE_DB_API_KEY = "USE_YOUR_OWN_CODE"
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app) # Initialize Bootstrap for styling

# --- Database Configuration ---
# Define the base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass
# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app) # Initialize the database with the app


# --- Database Table Model ---
# This class defines the structure of the 'movie' table in the database
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    # rating, ranking, and review can be NULL initially
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# Create the database table if it doesn't exist
with app.app_context():
    db.create_all()


# --- Forms ---
# Form for searching for a new movie to add
class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

# Form for editing a movie's rating and review
class RateMovieForm(FlaskForm):
    # FIXED: Changed from StringField to FloatField for numeric input.
    # Added validators to ensure the input is a number between 0 and 10.
    rating = FloatField(
        "Your Rating Out of 10 e.g. 7.5",
        validators=[DataRequired(), NumberRange(min=0, max=10)]
    )
    review = StringField("Your Review")
    submit = SubmitField("Done")


# --- Flask Routes ---
@app.route("/")
def home():
    """Renders the main page with all movies, ranked by rating."""
    # FIXED: Query now orders movies by rating in descending order.
    # `nulls_last()` ensures that unrated movies are at the bottom of the list.
    result = db.session.execute(db.select(Movie).order_by(desc(Movie.rating).nulls_last()))
    all_movies = result.scalars().all()

    # FIXED: Re-calculate ranks based on the corrected sorting order.
    # The highest-rated movie will be first (i=0) and get rank 1.
    for i in range(len(all_movies)):
        all_movies[i].ranking = i + 1
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    """Handles adding a new movie by searching the TMDB API."""
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        # Make a request to the TMDB API to search for the movie
        response = requests.get(MOVIE_DB_SEARCH_URL, params={
                                "api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        # Render a page for the user to select the correct movie from the results
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    """Finds movie details from TMDB API and adds it to the local database."""
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        # Get detailed movie info using its API ID
        response = requests.get(movie_api_url, params={
                                "api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        # Create a new Movie object with the fetched data
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0], # Extract the year
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        # Redirect the user to rate the movie they just added
        return redirect(url_for("rate_movie", id=new_movie.id))


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    """Handles editing a movie's rating and review."""
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id) # Get movie or return 404 error
    if form.validate_on_submit():
        # FIXED: `form.rating.data` is now safely a float due to form validation.
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete_movie():
    """Deletes a movie from the database."""
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)