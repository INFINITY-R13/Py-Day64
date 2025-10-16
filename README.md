# Top 10 Movies - Flask Web Application

A Flask-based web application for managing and rating your favorite movies. Works out-of-the-box with sample movie data, and optionally integrates with The Movie Database (TMDB) API for real movie search.

## ✨ Features

- 🎬 **Instant Setup** - Works immediately with built-in sample movies
- 🔍 **Smart Search** - Search sample movies or real TMDB database
- ⭐ **Movie Rating** - Rate movies on a scale of 0-10
- 📝 **Personal Reviews** - Write and save your movie reviews
- 🏆 **Auto Ranking** - Movies automatically ranked by your ratings
- 🗑️ **Easy Management** - Add, edit, and delete movies from your collection
- 📱 **Responsive Design** - Beautiful Bootstrap UI that works on all devices
- 🔄 **Graceful Fallback** - API failures automatically fall back to sample data

## 🚀 Quick Start

**Ready to use in 2 steps:**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python main.py
   ```

That's it! Open `http://localhost:5000` and start rating movies.

## 🎬 Sample Movies Included

The app comes with 5 classic movies ready to rate:
- The Shawshank Redemption (1994)
- The Godfather (1972) 
- Pulp Fiction (1994)
- Inception (2010)
- The Matrix (1999)

## 🔑 Optional: Real Movie Database

Want access to thousands of real movies? Set up a free TMDB API key:

1. **Get API Key:**
   - Sign up at [themoviedb.org](https://www.themoviedb.org/) (free)
   - Go to Settings > API and copy your key

2. **Configure:**
   ```bash
   # Windows
   set TMDB_API_KEY=your_actual_api_key_here
   
   # Mac/Linux  
   export TMDB_API_KEY=your_actual_api_key_here
   ```
   
   Or create a `.env` file:
   ```
   TMDB_API_KEY=your_actual_api_key_here
   ```

The app automatically detects the API key and switches to real movie search!

## 📖 How to Use

1. **Start the app:** `python main.py`
2. **Open browser:** Go to `http://localhost:5000`
3. **Add movies:** Click "Add Movie" and search (try "matrix" or "godfather")
4. **Rate & review:** Select a movie and give it a rating out of 10
5. **View collection:** See your ranked movie list on the home page
6. **Manage:** Edit ratings or delete movies anytime

## 🎯 Demo Mode vs Real API

| Feature | Demo Mode (No API Key) | Real API Mode |
|---------|----------------------|---------------|
| **Setup** | ✅ Instant - no configuration | ⚙️ Requires free TMDB account |
| **Movies Available** | 5 classic movies | 🌟 Millions of movies |
| **Search** | Matches from sample set | 🔍 Full text search |
| **Movie Data** | High-quality sample data | 📊 Complete movie database |
| **Posters** | ✅ Real movie posters | ✅ Real movie posters |

## 📁 Project Structure

```
├── main.py              # 🐍 Main Flask application with mock data
├── requirements.txt     # 📦 Python dependencies  
├── instance/
│   └── movies.db       # 🗄️ SQLite database (auto-created)
├── templates/          # 🎨 HTML templates
│   ├── base.html       # Base layout
│   ├── index.html      # Home page with movie cards
│   ├── add.html        # Movie search form
│   ├── edit.html       # Rating & review form
│   └── select.html     # Movie selection page
└── static/css/
    └── styles.css      # 💅 Custom styling
```

## 🛠️ Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Flask 3.1.2 | Web framework |
| **Database** | SQLAlchemy + SQLite | Data persistence |
| **Forms** | WTForms + Flask-WTF | Form handling & validation |
| **Frontend** | Bootstrap 5 | Responsive UI |
| **API** | TMDB API (optional) | Real movie data |
| **Styling** | Custom CSS | Movie card animations |

## 🗄️ Database Schema

Simple SQLite database with one `Movie` table:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `title` | String(250) | Movie title |
| `year` | Integer | Release year |
| `description` | String(500) | Movie plot summary |
| `rating` | Float | Your rating (0-10) |
| `ranking` | Integer | Auto-calculated rank |
| `review` | String(250) | Your personal review |
| `img_url` | String(250) | Movie poster URL |

## 🤝 Contributing

This is a learning project, but improvements are welcome! Feel free to:
- Report bugs
- Suggest features  
- Submit pull requests
- Share your movie collections

## 📄 License

Open source under the MIT License. Use it, modify it, learn from it!