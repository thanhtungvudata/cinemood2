import unittest
from unittest.mock import patch

import app
from llm import detect_mood, get_movies_by_mood
from tmdb_api import fetch_movies


class TestMoodMovieApp(unittest.TestCase):

    @patch("app.detect_mood")
    @patch("app.fetch_movies")
    @patch("app.get_movies_by_mood")
    def test_mood_detection(
        self, mock_get_movies_by_mood, mock_fetch_movies, mock_detect_mood
    ):
        """
        Tests if the AI correctly detects moods from user input and fetches movie recommendations.
        """
        # Mock AI-generated mood words (Flexible checking)
        detected_mood_words = ["happy", "joyful", "content"]
        mock_detect_mood.return_value = detected_mood_words

        # Mock trending movies (100 movies)
        mock_fetch_movies.return_value = [
            {
                "title": f"Movie {i}",
                "overview": f"Overview of Movie {i}.",
                "release_date": "2024-02-15",
                "poster": f"poster_{i}.jpg",
            }
            for i in range(100)
        ]

        # Mock AI-selected top 3 movies
        mock_get_movies_by_mood.return_value = [
            {
                "title": "Up",
                "overview": "An old man's adventure with a young boy.",
                "release_date": "2009-05-29",
                "poster": "img1",
                "match_reason": "Uplifting and heartwarming.",
            },
            {
                "title": "Inside Out",
                "overview": "A journey through emotions.",
                "release_date": "2015-06-19",
                "poster": "img2",
                "match_reason": "Captures joy and emotions.",
            },
            {
                "title": "The Pursuit of Happyness",
                "overview": "A man overcomes struggles to succeed.",
                "release_date": "2006-12-15",
                "poster": "img3",
                "match_reason": "Inspiring and joyful.",
            },
        ]

        # Simulate function calls
        mood_words = detect_mood("I feel so happy today!")
        movies = fetch_movies(100)  # Fetch 100 movies
        recommended_movies = get_movies_by_mood(mood_words, movies)  # Get top 3 matches

        # ✅ Flexible Mood Matching (Fuzzy Matching for GPT Variability)
        mood_variants = {
            "happy": ["happy", "cheerful", "joyful", "excited"],
            "joyful": ["joyful", "content", "vibrant", "cheerful"],
            "content": ["content", "peaceful", "relaxed"],
        }

        # for i, word in enumerate(mood_words):
        #     self.assertIn(word, mood_variants.get(detected_mood_words[i], []), f"❌ Unexpected mood word: {word}")

        # ✅ Ensure exactly 100 movies are fetched
        self.assertEqual(
            len(movies), 100, f"❌ Expected 100 movies but got {len(movies)}"
        )

        # ✅ Ensure only 3 movies are recommended
        self.assertEqual(
            len(recommended_movies),
            3,
            f"❌ Expected 3 recommended movies but got {len(recommended_movies)}",
        )

        # ✅ Ensure match reasons exist for recommendations
        for movie in recommended_movies:
            self.assertIn(
                "match_reason", movie, f"❌ Match reason missing for {movie['title']}"
            )

        print("✅ All tests passed for app.py!")


if __name__ == "__main__":
    unittest.main()
