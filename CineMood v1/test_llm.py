import unittest
from unittest.mock import patch

from llm import detect_mood, get_movies_by_mood


class TestLLMFunctions(unittest.TestCase):

    def test_detect_mood(self):
        """Test if detect_mood correctly returns 3 mood words."""
        test_cases = [
            ("I feel so happy today!", ["happy", "cheerful", "positive"]),
            ("I'm feeling a bit sad and down.", ["sad", "melancholy", "downcast"]),
            (
                "Feeling pumped and ready to go!",
                ["excited", "energetic", "enthusiastic"],
            ),
            (
                "I just remembered my childhood.",
                ["nostalgic", "sentimental", "reflective"],
            ),
            ("I want to explore new things!", ["curious", "adventurous", "eager"]),
            ("I'm very calm and at peace.", ["relaxed", "serene", "peaceful"]),
        ]

        for user_input, expected_moods in test_cases:
            detected_moods = detect_mood(user_input)
            self.assertEqual(
                len(detected_moods),
                3,
                f"❌ Expected 3 mood words but got {detected_moods}",
            )
            self.assertIsInstance(
                detected_moods, list, "❌ Expected a list of mood words"
            )
            print(
                f"✅ Mood detection passed for input: '{user_input}' → {detected_moods}"
            )

    def test_match_movie_to_mood(self):
        """Test if get_movies_by_mood selects the best 3 movies and provides explanations."""
        mood_words = ["happy", "inspired", "uplifting"]
        # Sample movies
        movies = [
            {
                "title": "Forrest Gump",
                "overview": "A man with a kind heart experiences major historical events.",
                "release_date": "1994-07-06",
            },
            {
                "title": "The Pursuit of Happyness",
                "overview": "A struggling father finds success through hard work and persistence.",
                "release_date": "2006-12-15",
            },
            {
                "title": "Up",
                "overview": "An old man goes on an adventure with a young boy scout and a talking dog.",
                "release_date": "2009-05-29",
            },
            {
                "title": "Joker",
                "overview": "A man slowly loses himself to his dark thoughts, leading to chaos.",
                "release_date": "2019-10-04",
            },
            {
                "title": "La La Land",
                "overview": "A romantic and musical journey of two aspiring artists.",
                "release_date": "2016-12-09",
            },
        ]

        best_movies = get_movies_by_mood(mood_words, movies)

        # Check we got exactly 3 movies back
        self.assertEqual(
            len(best_movies),
            3,
            f"❌ Expected 3 recommended movies but got {len(best_movies)}",
        )
        for movie in best_movies:
            self.assertIn(
                "match_reason", movie, f"❌ Match reason missing for {movie['title']}"
            )
            print(f"✅ Recommended Movie: {movie['title']} → {movie['match_reason']}")


if __name__ == "__main__":
    unittest.main()
