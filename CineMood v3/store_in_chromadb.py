import json
import os
import time
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from config import OPENAI_API_KEY

# **Local storage for ChromaDB**
chroma_path = "chroma_db"
os.makedirs(chroma_path, exist_ok=True)

# **Initialize OpenAI Embeddings**
embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# **Define valid moods**
valid_moods = [
    "happy", "joyful", "cheerful", "delighted", "gleeful", "content", "lighthearted", "beaming",
    "excited", "thrilled", "exhilarated", "ecstatic", "overjoyed", "pumped", "hyped", "giddy",
    "grateful", "thankful", "appreciative", "blessed", "fulfilled", "satisfied",
    "hopeful", "optimistic", "encouraged", "expectant", "inspired",
    "loving", "affectionate", "romantic", "caring", "devoted", "tender",
    "peaceful", "calm", "serene", "tranquil", "relaxed", "mellow",
    "proud", "accomplished", "confident", "empowered", "self-assured",
    "sad", "melancholic", "gloomy", "heartbroken", "dejected", "sorrowful",
    "lonely", "isolated", "abandoned", "rejected", "homesick", "neglected",
    "hopeless", "despairing", "pessimistic", "defeated", "discouraged",
    "bored", "indifferent", "unenthusiastic", "unstimulated", "listless",
    "guilty", "remorseful", "regretful", "ashamed", "embarrassed",
    "tired", "fatigued", "drained", "exhausted", "sluggish",
    "angry", "furious", "enraged", "irritated", "resentful", "bitter",
    "frustrated", "annoyed", "exasperated", "impatient", "aggravated",
    "jealous", "envious", "covetous", "possessive", "insecure",
    "disgusted", "repulsed", "revolted", "grossed out", "nauseated",
    "anxious", "nervous", "worried", "uneasy", "apprehensive", "jittery",
    "fearful", "terrified", "panicked", "paranoid", "tense", "alarmed",
    "overwhelmed", "stressed", "pressured", "frazzled", "overloaded",
    "surprised", "shocked", "amazed", "astonished", "stunned", "flabbergasted",
    "confused", "perplexed", "puzzled", "disoriented", "unsure", "uncertain",
    "indecisive", "conflicted", "hesitant", "torn", "ambivalent",
    "neutral", "indifferent", "meh", "emotionless", "numb",
    "bittersweet", "nostalgic", "wistful", "sentimental", "pensive",
    "thoughtful", "introspective", "brooding", "deep in thought"
]

# **Compute embeddings for valid moods**
print("🔄 Generating embeddings for valid moods...")
mood_texts = valid_moods
mood_embeddings = embedding_model.embed_documents(mood_texts)

mood_store = Chroma(
    persist_directory=chroma_path,
    embedding_function=embedding_model,
    collection_name="valid_moods"
)
mood_store.add_texts(
    texts=mood_texts,
    metadatas=[{"mood": mood} for mood in valid_moods]
)
print(f"✅ Stored {len(valid_moods)} mood embeddings in ChromaDB ('valid_moods' collection).")

# **Load movie embeddings from JSON**
print("🔄 Loading movie metadata...")
with open("movie_embeddings.json", "r", encoding="utf-8") as f:
    movie_embeddings = json.load(f)

# **Helper function to process metadata safely**
def safe_join(value):
    if isinstance(value, list):
        return ", ".join(map(str, value))
    return str(value)

# **Convert movie metadata into LangChain Document format**
print("🔄 Storing movies in ChromaDB...")
documents = []
total_movies = len(movie_embeddings)
for index, movie in enumerate(movie_embeddings, start=1):
    metadata = movie.get("metadata", {})
    doc_metadata = {
        "title": safe_join(movie.get("title", "Unknown")),
        "overview": safe_join(metadata.get("overview", "Unknown")),
        "genres": safe_join(metadata.get("genres", [])),
        "main_cast": safe_join(metadata.get("main_cast", [])),
        "director": safe_join(metadata.get("director", "Unknown")),
        "tagline": safe_join(metadata.get("tagline", "Unknown")),
        "production_countries": safe_join(metadata.get("production_countries", [])),
        "keywords": safe_join(metadata.get("keywords", [])),
        "runtime": safe_join(metadata.get("runtime", "Unknown")),
        "production_companies": safe_join(metadata.get("production_companies", [])),
        "poster_path": safe_join(metadata.get("poster_path", "Unknown")),  # Ensure poster_path is included
        "release_date": safe_join(metadata.get("release_date", "Unknown"))  # Ensure release_date is included
    }
    page_content = f"{doc_metadata['title']} {doc_metadata['overview']}"
    documents.append(Document(page_content=page_content, metadata=doc_metadata))
    if index % 10 == 0 or index == total_movies:
        print(f"✅ Processed {index}/{total_movies} movies...")
    time.sleep(0.05)

movie_store = Chroma.from_documents(
    documents,
    embedding_model,
    persist_directory=chroma_path,
    collection_name="movies"
)
print(f"✅ ChromaDB successfully updated and stored at: {chroma_path}")
