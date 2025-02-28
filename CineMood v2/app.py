import streamlit as st
from llm import detect_mood, get_movies_by_mood
from tmdb_api import fetch_movies

def run_app():
    """
    Runs the Streamlit app for mood-based movie recommendations.
    Handles cases where detect_mood() returns only 2 values.
    """
    st.set_page_config(
        page_title="🎬 Mood-Based Movie Recommendation", 
        layout="centered"
    )

    st.title("🎬 CineMood: Get Mood-Based Trending Movies! ⚡")

    user_mood = st.text_area(
        "💬 How do you feel right now?",
        st.session_state.get("user_mood", ""),
        height=100
    )

    if st.button("Find Movies"):
        if user_mood.strip():
            with st.spinner("🔍 Analyzing your mood..."):
                valid_moods, extracted_words, detected_moods = detect_mood(user_mood)

            if valid_moods == ["invalid"]:
                st.warning("⚠️ That doesn't look like a mood. Please describe how you're feeling.")
            else:
                st.success(f"🤖 AI Detected Moods: {', '.join(valid_moods).title()}")

                with st.spinner("🎥 Fetching movies and ranking matches..."):
                    movies = fetch_movies(60)

                    if valid_moods == ["neutral", "neutral", "neutral"]:
                        st.info("🎭 We couldn't be sure about your moods, so let us guess. Here are some trending movies you might enjoy!")

                        if extracted_words:
                            st.write(f"🔍 AI detected these key words from your input: **{', '.join(extracted_words)}**")
                            recommended_movies = get_movies_by_mood(extracted_words, movies)
                        else:
                            recommended_movies = movies[:3]
                    else:
                        recommended_movies = get_movies_by_mood(valid_moods, movies)

                if recommended_movies:
                    for movie in recommended_movies:
                        st.subheader(movie["title"])
                        st.write(f"📅 Release Date: {movie['release_date']}")
                        st.write(f"🎭 Match Reason: {movie.get('match_reason', 'Trending movie recommendation.')}")
                        if movie["poster"]:
                            st.image(movie["poster"], width=200)
                        st.write(f"📜 Overview: {movie['overview']}")
                        st.markdown("---")
                else:
                    st.warning("⚠️ No suitable movie recommendations found.")
        else:
            st.warning("⚠️ Please enter how you feel to get movie recommendations.")

    st.markdown("**Made by [Thanh Tung Vu](https://thanhtungvudata.github.io/)**")

if __name__ == "__main__":
    run_app()
