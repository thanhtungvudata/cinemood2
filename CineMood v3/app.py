import streamlit as st
import numpy as np
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config import OPENAI_API_KEY
from PIL import Image
import requests
from io import BytesIO

def run_app():
    """
    Runs the Streamlit app for mood-based movie recommendations.
    """
    # **Initialize OpenAI Embeddings & ChromaDB**
    chroma_path = "chroma_db"
    embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    vector_store = Chroma(
        persist_directory=chroma_path,
        embedding_function=embedding_model,
        collection_name="movies"
    )

    mood_store = Chroma(
        persist_directory=chroma_path,
        embedding_function=embedding_model,
        collection_name="valid_moods"
    )

    client = OpenAI(api_key=OPENAI_API_KEY)

    # **Helper function to compute cosine similarity**
    def cosine_similarity(vec1, vec2):
        """Computes cosine similarity between two vectors, handling division by zero."""
        norm1, norm2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
        return np.dot(vec1, vec2) / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0

    # **Function to get the closest mood**
    def get_top_mood(user_input):
        user_mood_vector = embedding_model.embed_query(user_input)
        mood_retriever = mood_store.as_retriever(search_kwargs={"k": 5})
        valid_mood_results = mood_retriever.invoke(user_input)

        similarities = []
        unique_moods = set()
        
        for mood in valid_mood_results:
            mood_name = mood.metadata.get("mood", "").lower()
            if mood_name not in unique_moods:  # Ensure uniqueness
                mood_vector = embedding_model.embed_query(mood_name)
                similarity_score = cosine_similarity(user_mood_vector, mood_vector)
                similarities.append((mood_name, similarity_score))
                unique_moods.add(mood_name)

        similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:3]

        if not similarities or similarities[0][1] < 0.8:
            return None  # No valid moods found

        return [mood[0] for mood in similarities]  # Return top 3 distinct moods

    # **Function to get unique movie recommendations**
    def get_movie_recommendations(detect_moods):
        retriever = vector_store.as_retriever(search_kwargs={"k": 10})
        results = retriever.invoke(detect_moods)

        unique_movies = {}
        for movie in results:
            title = movie.metadata.get("title", "Unknown")
            if title not in unique_movies:
                unique_movies[title] = movie

        return list(unique_movies.values())[:3]  # Return only top 3 unique movies

    # **Function to generate LLM-based explanation**
    def generate_explanation(detect_moods, user_input, movie):
        movie_description = (
            f"{movie.metadata.get('title', 'Unknown')} ({movie.metadata.get('genres', 'Unknown')})\n"
            f"Overview: {movie.metadata.get('overview', 'No overview available')}\n"
        )

        explanation_prompt = f"""
        A user said {user_input} and might be feeling {detect_moods}. Based on what they said and their moods, here is the recommended movie:

        {movie_description}

        Generate a friendly, engaging movie recommendation explanation that highlights why this movie might be a good fit for the user.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful movie recommendation assistant."},
                {"role": "user", "content": explanation_prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    # **Function to fetch movie poster**
    def get_movie_poster(url):
        """Fetches movie poster from URL, returns None if invalid."""
        if not url or not url.startswith("http"):
            return None  # Invalid or missing URL

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                return image
        except requests.exceptions.RequestException:
            return None  # Return None if request fails

        return None  # Default fallback if nothing works

    # **Streamlit UI**
    st.title("🎬 CineMood: Get Mood-Based Trending Movies! ⚡")

    st.write("Enter how you're feeling right now, and we'll recommend the best movies for you!")

    user_input = st.text_input("How are you feeling now?", placeholder="E.g., happy, nostalgic, adventurous, I am missing my lovely daughter, etc.")

    if st.button("🎥 Recommend Movies"):
        if not user_input:
            st.warning("⚠️ Please enter how you're feeling.")
        else:
            with st.spinner("Detecting your mood and finding the best movies for you..."):
                detect_moods = get_top_mood(user_input)

                if not detect_moods:
                    st.warning("⚠️ Oh, I’m not quite sure I caught that mood! Could you share how you're feeling in another way? I'd love to find the perfect movie for you!")
                else:
                    st.success(f"🤖 Detected Moods: {', '.join(detect_moods)}")

                    # Use only the first mood for movie recommendations
                    top_movies = get_movie_recommendations(detect_moods[0])

                    if not top_movies:
                        st.error("❌ No relevant movies found for your mood.")
                    else:
                        # explanation = generate_explanation(detect_moods[0], user_input, top_movies)

                        st.markdown("## 🎬 **Top 3 Movie Recommendations**")

                        for i, movie in enumerate(top_movies):
                            metadata = movie.metadata
                            st.subheader(f"{i+1}. {metadata.get('title', 'Unknown')} ({metadata.get('genres', 'Unknown')})")
                            st.write(f"**📅 Release Date:** {metadata.get('release_date', 'Unknown')}")
                            st.write(f"**🎭 Cast:** {metadata.get('main_cast', 'Unknown')}")
                            st.write(f"**🎬 Director:** {metadata.get('director', 'Unknown')}")
                            st.write(f"**🏷️ Tagline:** {metadata.get('tagline', 'Unknown')}")
                            st.write(f"**🌍 Country:** {metadata.get('production_countries', 'Unknown')}")
                            st.write(f"**🏢 Production Company:** {metadata.get('production_companies', 'Unknown')}")
                            st.write(f"**⏳ Runtime:** {metadata.get('runtime', 'Unknown')} min")

                            poster_url = metadata.get('poster_path', '')
                            if poster_url:
                                image = get_movie_poster(poster_url)
                                if image:
                                    st.image(image, width=200)
                                else:
                                    st.warning("⚠️ Poster not available.")
                            
                            explanation = generate_explanation(detect_moods[0], user_input, movie)
                            st.write(explanation)

                            st.write("---")

    st.markdown("**Made by [Thanh Tung Vu](https://thanhtungvudata.github.io/)**")

if __name__ == "__main__":
    run_app()
                        

