import datetime
import requests

from config import TMDB_API_KEY


def get_first_day_of_week():
    """Returns the first day (Monday) of the current week."""
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday())


def fetch_movies(max_movies=100):
    """
    Fetch up to `max_movies` trending movies, ensuring only movies with release dates before the first day
    of the current week are considered, and that they have non-empty overviews.
    Returns the movies sorted by release date (latest first).
    """
    movies = []
    pages_to_fetch = (max_movies // 20) + 1
    first_day_of_week = get_first_day_of_week()

    for page in range(1, pages_to_fetch + 1):
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}&language=en-US&page={page}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for movie in data.get("results", []):
                release_date = movie.get("release_date", "9999-12-31")
                overview = movie.get("overview", "").strip()
                try:
                    release_date_obj = datetime.datetime.strptime(release_date, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if overview and release_date_obj < first_day_of_week:
                    movies.append({
                        "title": movie["title"],
                        "overview": overview,
                        "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                        "release_date": release_date,
                    })
            if len(movies) >= max_movies:
                break
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error fetching movies: {e}")
            break

    return sorted(movies, key=lambda x: x["release_date"], reverse=True)[:max_movies]
