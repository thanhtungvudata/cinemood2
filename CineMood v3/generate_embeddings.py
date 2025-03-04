import json
import time
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY

# Load TMDB movie data from the previous step
with open("trending_movies.json", "r") as f:
    movies = json.load(f)

# Initialize LangChain OpenAI Embedding model
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def generate_movie_embedding(movie):
    """Generate embeddings for a movie using LangChain's OpenAIEmbeddings."""
    text_data = f"""
    Title: {movie.get('title', 'Unknown')}
    Overview: {movie.get('overview', 'No overview available')}
    Genres: {', '.join(movie.get('genres', []))}
    Main Cast: {', '.join(movie.get('main_cast', []))}
    Director: {movie.get('director', 'Unknown')}
    Tagline: {movie.get('tagline', 'No tagline available')}
    Production Countries: {', '.join(movie.get('production_countries', []))}
    Keywords: {', '.join(movie.get('keywords', []))}
    Runtime: {movie.get('runtime', 'Unknown')} minutes
    Production Companies: {', '.join(movie.get('production_companies', []))}
    Release Date: {movie.get('release_date', 'Unknown')}
    """
    
    return embedding_model.embed_query(text_data)

# Generate embeddings for all movies
movie_embeddings = []
total_movies = len(movies)
print(f"🔄 Generating embeddings for {total_movies} movies...")

for index, movie in enumerate(movies, start=1):
    embedding = generate_movie_embedding(movie)
    movie_embeddings.append({
        "id": movie.get("id", "Unknown"),
        "title": movie.get("title", "Unknown"),
        "embedding": embedding,
        "metadata": {
            "overview": movie.get("overview", "No overview available"),
            "genres": ", ".join(movie.get("genres", [])),
            "main_cast": ", ".join(movie.get("main_cast", [])),
            "director": movie.get("director", "Unknown"),
            "tagline": movie.get("tagline", "No tagline available"),
            "production_countries": ", ".join(movie.get("production_countries", [])),
            "keywords": ", ".join(movie.get("keywords", [])),
            "runtime": movie.get("runtime", "Unknown"),
            "production_companies": ", ".join(movie.get("production_companies", [])),
            "poster_path": movie.get("poster_path", None),  # Ensure poster_path is included
            "release_date": movie.get("release_date", "Unknown")  # Added release_date
        }
    })
    
    if index % 10 == 0 or index == total_movies:
        print(f"✅ Processed {index}/{total_movies} movies...")

# Save embeddings for later use
with open("movie_embeddings.json", "w") as f:
    json.dump(movie_embeddings, f, indent=4)

print("✅ Embeddings successfully generated and saved!")
