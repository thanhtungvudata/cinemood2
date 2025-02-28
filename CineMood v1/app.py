import streamlit as st

from llm import detect_mood, get_movies_by_mood
from tmdb_api import fetch_movies

st.set_page_config(
    page_title="🎬 Mood-Based Trending Movie Recommendation", layout="centered"
)

st.title("🎬 CineMood2: Get your Mood-based Trending Movies!⚡")

user_mood = st.text_area("💬 How do you feel right now?", st.session_state.get("user_mood", ""), height=100)

if st.button("Find Movies"):
    if user_mood.strip():
        with st.spinner("🔍 Analyzing your mood..."):
            mood_words = detect_mood(user_mood)
        st.success(f"🤖 AI Detected Moods: {', '.join(mood_words).title()}")

        with st.spinner("🎥 Fetching movies and ranking matches..."):
            movies = fetch_movies(60)
            recommended_movies = get_movies_by_mood(mood_words, movies)

        if recommended_movies:
            for movie in recommended_movies:
                st.subheader(movie["title"])
                st.write(f"📅 Release Date: {movie['release_date']}")
                st.write(f"🎭 Match Reason: {movie['match_reason']}")
                if movie["poster"]:
                    st.image(movie["poster"], width=200)
                st.write(f"📜 Overview: {movie['overview']}")
                st.markdown("---")
        else:
            st.warning("⚠️ No suitable movie recommendations found.")
    else:
        st.warning("⚠️ Please enter how you feel to get movie recommendations.")

# Footer Section
st.markdown("**Made by [Thanh Tung Vu](https://thanhtungvudata.github.io/)**")
