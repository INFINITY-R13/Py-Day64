# Top 10 Movies - Flask Web Application

A Flask-based web application for managing and rating your favorite movies. This app integrates with The Movie Database (TMDB) API to search and add movies, then allows you to rate and review them.

## Features

- 🎬 Search and add movies from TMDB database
- ⭐ Rate movies on a scale of 0-10
- 📝 Write personal reviews
- 🏆 Automatic ranking based on ratings
- 🗑️ Delete movies from your collection
- 📱 Responsive Bootstrap UI

## Screenshots

The application displays your top-rated movies in an attractive card layout with movie posters, ratings, and reviews.

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get your TMDB API key:
   - Sign up at [themoviedb.org](https://www.themoviedb.org/)
   - Go to Settings > API
   - Copy your API key

4. Update the API key in `main.py`:
   ```python
   MOVIE_DB_API_KEY = "your_actual_api_key_here"
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Click "Add Movie" to search for movies
4. Select the correct movie from search results
5. Rate and review your movie
6. View your ranked collection on the home page

## Project Structure

```
├── main.py              # Main Flask application
├── requirements.txt     # Python dependencies
├── movies.db           # SQLite database (created automatically)
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   ├── add.html        # Add movie form
│   ├── edit.html       # Edit rating form
│   └── select.html     # Movie selection page
└── static/
    └── css/
        └── styles.css  # Custom styles
```

## Technologies Used

- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **WTForms** - Form handling and validation
- **Bootstrap** - UI framework
- **TMDB API** - Movie data source
- **SQLite** - Database

## API Integration

This app uses The Movie Database (TMDB) API to:
- Search for movies by title
- Fetch movie details (poster, description, release date)
- Get high-quality movie poster images

## Database Schema

The app uses a simple SQLite database with a `Movie` table containing:
- `id` - Primary key
- `title` - Movie title
- `year` - Release year
- `description` - Movie overview
- `rating` - Your personal rating (0-10)
- `ranking` - Auto-calculated rank
- `review` - Your personal review
- `img_url` - Movie poster URL

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.