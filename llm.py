import json

import openai

from config import OPENAI_API_KEY

# Initialize OpenAI API client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def detect_mood(user_input):
    """
    Uses GPT-4o-mini to detect mood from user input.
    Returns exactly 3 descriptive mood words.
    """
    prompt = f"""
    Analyze the following user input and determine the three best words to describe the mood.

    User input: "{user_input}"
    
    Respond with exactly 3 words, separated by commas.
    Example: happy, joyful, excited.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "system", "content": prompt}]
        )
        mood_words = response.choices[0].message.content.strip().lower().split(", ")
        return mood_words if len(mood_words) == 3 else ["neutral", "neutral", "neutral"]
    except Exception as e:
        print(f"⚠️ Error with OpenAI API in detect_mood: {e}")
        return ["neutral", "neutral", "neutral"]


def get_movies_by_mood(mood_words, movies):
    """
    Uses GPT-4o-mini to rank movies based on how well their overview matches the detected mood words.
    Returns the top 3 movies with match explanations, sorted by release date (latest first).
    """
    if not movies:
        print("⚠️ No movies available to match moods.")
        return []

    movie_descriptions = "\n".join(
        [f"{i+1}. {m['title']}: {m['overview']}" for i, m in enumerate(movies)]
    )

    prompt = f"""
    You must output only valid JSON and nothing else.
    The JSON should be an array of exactly 3 objects.
    Each object must have two keys: "index" (an integer) and "match_reason" (a non-empty string).
    
    The user is in a mood described by these words: {", ".join(mood_words)}.
    
    Below are movie descriptions:
    {movie_descriptions}
    
    Select the top 3 movies that best match this mood and provide a brief explanation (1-2 sentences) for each.
    Respond strictly in JSON format:
    [
        {{"index": 1, "match_reason": "Explanation for movie 1"}},
        {{"index": 2, "match_reason": "Explanation for movie 2"}},
        {{"index": 3, "match_reason": "Explanation for movie 3"}}
    ]
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "system", "content": prompt}]
        )
        json_response = response.choices[0].message.content.strip()
        ranked_movies = json.loads(json_response)
        matched_movies = []
        default_explanation = "This movie appears to be a good match based on its emotional tone and themes."
        for entry in ranked_movies:
            index = entry.get("index", 0) - 1
            explanation = entry.get("match_reason", "").strip() or default_explanation
            if 0 <= index < len(movies):
                matched_movie = movies[index]
                matched_movie["match_reason"] = explanation
                matched_movies.append(matched_movie)
        # Ensure exactly 3 movies are returned by filling with fallbacks if necessary
        while len(matched_movies) < 3 and len(movies) >= 3:
            fallback = movies[len(matched_movies)]
            fallback["match_reason"] = default_explanation
            matched_movies.append(fallback)
        # Sort the matched movies by release date (latest first)
        matched_movies = sorted(
            matched_movies, key=lambda x: x["release_date"], reverse=True
        )
        return matched_movies[:3]
    except Exception as e:
        print(f"⚠️ Error ranking movies: {e}")
        fallback_movies = []
        default_explanation = "This movie appears to be a good match based on its emotional tone and themes."
        for m in movies[:3]:
            m["match_reason"] = default_explanation
            fallback_movies.append(m)
        fallback_movies = sorted(
            fallback_movies, key=lambda x: x["release_date"], reverse=True
        )
        return fallback_movies
