import unittest

from tmdb_api import fetch_movies


class TestTMDBAPI(unittest.TestCase):

    def test_fetch_100_movies(self):
        """Test if fetching movies correctly retrieves 100 movies."""
        movies = fetch_movies(max_movies=100)

        # Check if exactly 100 movies are returned
        self.assertEqual(
            len(movies), 100, f"Expected 100 movies, but got {len(movies)}"
        )

        # Ensure all movies have valid fields
        for movie in movies:
            self.assertIn("title", movie, "Missing title in movie data")
            self.assertIn("overview", movie, "Missing overview in movie data")
            self.assertIn("release_date", movie, "Missing release_date in movie data")
            self.assertTrue(
                isinstance(movie["title"], str) and movie["title"],
                "Invalid movie title",
            )
            self.assertTrue(
                isinstance(movie["overview"], str) and movie["overview"],
                "Invalid movie overview",
            )
            self.assertTrue(
                isinstance(movie["release_date"], str) and movie["release_date"],
                "Invalid movie release date",
            )


if __name__ == "__main__":
    unittest.main()
