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
import os

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, that's okay
    pass

# --- API Configuration ---
# You need to get your own API key from themoviedb.org
MOVIE_DB_API_KEY = os.environ.get('TMDB_API_KEY')
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# Check if API key is set
if not MOVIE_DB_API_KEY:
    print("⚠️  WARNING: TMDB_API_KEY environment variable not set!")
    print("   Using mock data for testing. Set TMDB_API_KEY for real functionality.")

# Mock movie data for testing when no API key is available
MOCK_MOVIES = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "release_date": "1994-09-23",
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg"
    },
    {
        "id": 2,
        "title": "The Godfather",
        "release_date": "1972-03-14",
        "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
    },
    {
        "id": 3,
        "title": "Pulp Fiction",
        "release_date": "1994-09-10",
        "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
        "poster_path": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"
    },
    {
        "id": 4,
        "title": "Inception",
        "release_date": "2010-07-16",
        "overview": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster_path": "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg"
    },
    {
        "id": 5,
        "title": "The Matrix",
        "release_date": "1999-03-30",
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
    }
]

# --- Flask App Initialization ---
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# CSRF is enabled by default for security
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
    """Handles adding a new movie by searching the TMDB API or using mock data."""
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data.lower()
        
        if MOVIE_DB_API_KEY:
            # Use real API
            try:
                response = requests.get(MOVIE_DB_SEARCH_URL, params={
                                        "api_key": MOVIE_DB_API_KEY, "query": movie_title})
                response.raise_for_status()
                data = response.json()["results"]
                return render_template("select.html", options=data)
            except (requests.RequestException, KeyError):
                # If API fails, fall back to mock data
                mock_results = MOCK_MOVIES
                return render_template("select.html", options=mock_results, 
                                     mock_mode=True, search_term=movie_title, 
                                     api_fallback=True)
        else:
            # Use mock data for testing
            mock_results = [movie for movie in MOCK_MOVIES 
                           if movie_title in movie["title"].lower()]
            
            if not mock_results:
                # If no matches, show all available movies
                mock_results = MOCK_MOVIES
                
            return render_template("select.html", options=mock_results, 
                                 mock_mode=True, search_term=movie_title)
    
    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    """Finds movie details from TMDB API or mock data and adds it to the local database."""
    movie_api_id = request.args.get("id")
    if movie_api_id:
        if MOVIE_DB_API_KEY:
            # Use real API
            try:
                movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
                response = requests.get(movie_api_url, params={
                                        "api_key": MOVIE_DB_API_KEY, "language": "en-US"})
                response.raise_for_status()
                data = response.json()
                new_movie = Movie(
                    title=data["title"],
                    year=data["release_date"].split("-")[0],
                    img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
                    description=data["overview"]
                )
                db.session.add(new_movie)
                db.session.commit()
                return redirect(url_for("rate_movie", id=new_movie.id))
            except (requests.RequestException, KeyError):
                # If API fails, redirect to home
                return redirect(url_for("home"))
        else:
            # Use mock data
            try:
                movie_id = int(movie_api_id)
                mock_movie = next((m for m in MOCK_MOVIES if m["id"] == movie_id), None)
                
                if mock_movie:
                    new_movie = Movie(
                        title=mock_movie["title"],
                        year=int(mock_movie["release_date"].split("-")[0]),
                        img_url=f"{MOVIE_DB_IMAGE_URL}{mock_movie['poster_path']}",
                        description=mock_movie["overview"]
                    )
                    db.session.add(new_movie)
                    db.session.commit()
                    return redirect(url_for("rate_movie", id=new_movie.id))
                else:
                    # Movie not found, redirect to home
                    return redirect(url_for("home"))
            except ValueError:
                # Invalid ID, redirect to home
                return redirect(url_for("home"))
    
    return redirect(url_for("home"))


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