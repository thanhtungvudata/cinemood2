import requests
import json
import time
from datetime import datetime, timedelta
from config import TMDB_API_KEY

# TMDB API Endpoints
TRENDING_URL = "https://api.themoviedb.org/3/trending/movie/week"
MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{movie_id}?api_key=" + TMDB_API_KEY + "&append_to_response=keywords"
CREDITS_URL = "https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=" + TMDB_API_KEY

# Calculate the first day of the current week
current_date = datetime.utcnow()
first_day_of_week = current_date - timedelta(days=current_date.weekday())
first_day_of_week_str = first_day_of_week.strftime("%Y-%m-%d")

def fetch_trending_movies(pages=10):
    """Fetch trending movies from multiple pages."""
    movies = []
    for page in range(1, pages + 1):
        response = requests.get(TRENDING_URL, params={"api_key": TMDB_API_KEY, "page": page})
        if response.status_code == 200:
            movies.extend(response.json().get("results", []))
        else:
            print(f"Error fetching movies from page {page}: {response.status_code}")
    return movies

def fetch_movie_details(movie_id):
    """Fetch full metadata for a movie including cast, crew, and keywords."""
    details_response = requests.get(MOVIE_DETAILS_URL.format(movie_id=movie_id))
    credits_response = requests.get(CREDITS_URL.format(movie_id=movie_id))
    
    if details_response.status_code == 200 and credits_response.status_code == 200:
        details = details_response.json()
        credits = credits_response.json()
        release_date = details.get("release_date")
        
        if release_date and release_date < first_day_of_week_str:
            return {
                "id": details.get("id"),
                "title": details.get("title"),
                "overview": details.get("overview"),
                "release_date": release_date,
                "popularity": details.get("popularity"),
                "vote_average": details.get("vote_average"),
                "vote_count": details.get("vote_count"),
                "genres": [genre["name"] for genre in details.get("genres", [])],
                "runtime": details.get("runtime"),
                "original_language": details.get("original_language"),
                "spoken_languages": [lang["english_name"] for lang in details.get("spoken_languages", [])],
                "status": details.get("status"),
                "budget": details.get("budget"),
                "revenue": details.get("revenue"),
                "production_companies": [company["name"] for company in details.get("production_companies", [])],
                "production_countries": [country["name"] for country in details.get("production_countries", [])],
                "tagline": details.get("tagline"),
                "homepage": details.get("homepage"),
                "imdb_id": details.get("imdb_id"),
                "poster_path": f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}" if details.get("poster_path") else None,
                "main_cast": [cast["name"] for cast in credits.get("cast", [])[:5]],
                "director": next((crew["name"] for crew in credits.get("crew", []) if crew["job"] == "Director"), "Unknown"),
                "keywords": [keyword["name"] for keyword in details.get("keywords", {}).get("keywords", [])],
            }
    else:
        print(f"Error fetching details for movie ID {movie_id}")
    return None

def get_trending_movies_with_details():
    """Fetch trending movies and their full metadata before the first day of the current week."""
    trending_movies = fetch_trending_movies(pages=10)
    movies_metadata = []
    total_movies = len(trending_movies[:200])
    print(f"🔄 Fetching details for {total_movies} movies...")
    
    for index, movie in enumerate(trending_movies[:200], start=1):
        movie_id = movie["id"]
        movie_details = fetch_movie_details(movie_id)
        
        if movie_details:
            movies_metadata.append(movie_details)
        
        if index % 10 == 0 or index == total_movies:
            print(f"✅ Processed {index}/{total_movies} movies...")
    
    return movies_metadata

if __name__ == "__main__":
    trending_movies_data = get_trending_movies_with_details()

    # Save data to a JSON file for use in embedding generation
    with open("trending_movies.json", "w") as f:
        json.dump(trending_movies_data, f, indent=4)

    print("\n✅ Trending movies saved to `trending_movies.json`")