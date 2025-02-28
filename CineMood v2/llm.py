import json
import openai
from config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ✅ Updated Mood List
VALID_MOOD_WORDS = set([
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
])

# ✅ Function to Map Detected Moods Using GPT
def map_to_valid_mood(mood_words):
    """
    Uses GPT to determine the closest valid moods from `VALID_MOOD_WORDS`.
    Ensures that:
    - The result contains **exactly 3 unique** moods.
    - All moods are from `VALID_MOOD_WORDS`.
    - If fewer than 3 moods are returned, "neutral" is added.
    """

    valid_moods_string = ", ".join(VALID_MOOD_WORDS)

    prompt = f"""
    You are an expert in understanding human emotions.
    Your task is to map the detected moods "{', '.join(mood_words)}" to the **three closest** valid moods from the predefined list below:

    {valid_moods_string}

    **Rules:**
    1. Select exactly **3 unique** moods from the list.
    2. If a mood is unrelated to any in the list, replace it with **"neutral"**.
    3. **Return ONLY a comma-separated list of 3 moods, no extra text.**
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        # ✅ Extract and clean GPT response
        mapped_moods = response.choices[0].message.content.strip().lower()

        # ✅ Handle cases where GPT incorrectly formats the output
        mapped_moods = mapped_moods.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
        mapped_moods = mapped_moods.split(", ")
        mapped_moods = [mood.strip() for mood in mapped_moods if mood in VALID_MOOD_WORDS]

        # ✅ Ensure exactly 3 unique moods
        unique_moods = list(dict.fromkeys(mapped_moods))  # Remove duplicates while keeping order

        # ✅ Fill with "neutral" if fewer than 3 moods are returned
        while len(unique_moods) < 3:
            unique_moods.append("neutral")

        return unique_moods[:3]  # Always return a single flat list of 3 moods

    except Exception as e:
        print(f"⚠️ Error in mapping mood: {e}")
        return ["neutral", "neutral", "neutral"]  # Default in case of error


# ✅ Function to Detect Mood
def detect_mood(user_input):
    """
    Detects mood from user input:
    - Extracts key words from the user's input.
    - Uses GPT to map detected moods to `VALID_MOOD_WORDS`.
    - Returns ['invalid'] for non-emotional input.
    """
    valid_moods_string = ", ".join(VALID_MOOD_WORDS)

    prompt = f"""
    Analyze the user input {user_input} and:
    If the input {user_input} has any words that are related to at least one of these words {valid_moods_string} or related to the nouns of {valid_moods_string}, return output as a **valid JSON object** with:
        - "detected_moods": **Always a list of exactly 3 different mood words that best describe the user's input {user_input}** 
        - "extracted_words": The key words you identified in the user's input {user_input}.

    If input {user_input} is **related to a mood** but not related to at least one of these words {valid_moods_string} or related to the nouns of {valid_moods_string}, return output as a **valid JSON object** with:
        - "detected_moods": **Always a list of exactly 3 different mood words that best describe the user's input {user_input}** 
        - "extracted_words": The key words you identified in the user's input {user_input}.

    If the input {user_input} is **COMPLETELY NOT related to a mood** (e.g., "What time is it?"), return output as a **valid JSON object** with:
        - "detected_moods": ["invalid"] 
        - "extracted_words": [].

    Example:
    User input: "I feel a bit lost and unsure what to do."
    Response:
    {{"detected_moods": ["melancholic", "uncertain", "conflicted"], "extracted_words": ["lost", "unsure"]}}

    User input: "What time is it?"
    Response:
    {{"detected_moods": ["invalid"], "extracted_words": []}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        json_response = json.loads(response.choices[0].message.content.strip())
        detected_moods = json_response.get("detected_moods", [])
        extracted_words = json_response.get("extracted_words", [])

        if detected_moods == ["invalid"]:
            return ["invalid"], [], []

        # ✅ Separate known moods from unknown moods
        known_moods = [mood for mood in detected_moods if mood in VALID_MOOD_WORDS]
        unknown_moods = [mood for mood in detected_moods if mood not in VALID_MOOD_WORDS]

        # ✅ Map unknown moods to valid moods using GPT only if necessary
        mapped_moods = map_to_valid_mood(unknown_moods) if unknown_moods else []

        # ✅ Combine known and mapped moods, ensuring 3 unique moods
        final_moods = list(dict.fromkeys(known_moods + mapped_moods))  # Remove duplicates

        while len(final_moods) < 3:
            final_moods.append("neutral")

        return final_moods[:3], extracted_words, detected_moods

    except json.JSONDecodeError:
        print("⚠️ Error: GPT returned invalid JSON.")
        return ["neutral", "neutral", "neutral"], [], []
    
    except Exception as e:
        print(f"⚠️ Error in detect_mood: {e}")
        return ["neutral", "neutral", "neutral"], [], []


def get_movies_by_mood(mood_words, movies):
    """
    Uses GPT to rank movies based on detected moods or extracted words.
    ✅ If mood is ["neutral", "neutral", "neutral"], match using extracted words.
    ✅ Otherwise, rank movies based on emotional relevance.
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
    
    The user’s detected moods: {", ".join(mood_words)}.
    
    Below are movie descriptions:
    {movie_descriptions}
    
    Select the top 3 movies that best match this mood or extracted words and provide a brief explanation (1-2 sentences) for each.
    Respond strictly in JSON format:
    [
        {{"index": 1, "match_reason": "Explanation for movie 1"}},
        {{"index": 2, "match_reason": "Explanation for movie 2"}},
        {{"index": 3, "match_reason": "Explanation for movie 3"}}
    ]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        json_response = json.loads(response.choices[0].message.content.strip())

        matched_movies = []
        for entry in json_response:
            index = entry["index"] - 1
            explanation = entry.get("match_reason", "Trending movie recommendation.")
            if 0 <= index < len(movies):
                matched_movie = movies[index]
                matched_movie["match_reason"] = explanation
                matched_movies.append(matched_movie)

        return matched_movies

    except Exception as e:
        print(f"⚠️ Error ranking movies: {e}")
        return movies[:3]  # Default to trending movies