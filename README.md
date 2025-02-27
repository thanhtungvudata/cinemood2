# 🎬 CineMood2 - AI-Powered Mood-Based Movie Recommendations  

CineMood2 is an AI agent-based movie recommendation system that helps users find trending movies based on their mood. It leverages **GPT-4o-mini** for mood detection and movie ranking, and **TMDB API** for fetching trending movies.


## 🚀 Demo

🎭 **Try the app:** [CineMood2: AI-Agent-Assisted Mood-Based Movie Recommendation](https://huggingface.co/spaces/thanhtungvudata/cinemoodv2)  
📝 **Blog post:** [AI-Agent-Assisted Mood-Based Movie Recommendation]([https://medium.com/@tungvu_37498/from-api-to-app-creating-a-mood-based-trending-movie-recommender-with-python-hugging-face-model-e32d67b492e2](https://medium.com/@tungvu_37498/ai-agent-assisted-mood-based-movie-recommendation-086a382cf3fb))
---

## 🚀 Features  
✅ **Mood Detection**: Uses GPT-4o-mini to extract 3 mood words from user input.  
✅ **Trending Movie Fetching**: Retrieves **100 trending movies** from TMDB, filtering only past releases.  
✅ **AI-Based Matching**: Finds the **top 3** movies that best match the user's mood.  
✅ **Real-time Recommendations**: Always up-to-date with the latest trending movies.  
✅ **Easy to Use**: Runs on **Streamlit** with an intuitive UI.  
✅ **Dockerized Deployment**: Ensures smooth operation across environments.

---

## 🛠 Tech Stack  

| Technology   | Purpose |
|-------------|---------|
| **GPT-4o-mini** | Mood detection & movie ranking |
| **TMDB API** | Fetching trending movies |
| **Python** | Backend logic |
| **Streamlit** | Frontend UI |
| **Docker** | Containerization |
| **VSCode** | Development |
| **Git & GitHub** | Version control |
| **Flake8** | Code linting |
| **pytest** | Automated testing |

---

## 📌 How It Works  

### **1️⃣ User Inputs Mood**
Users enter how they feel in a **text box** in the Streamlit UI.

### **2️⃣ GPT-4o-mini Detects Mood**
The input is sent to **GPT-4o-mini**, which returns **3 mood words** describing the user's feelings.

### **3️⃣ Fetch Trending Movies**
CineMood2 uses **TMDB API** to fetch **100 trending movies**, filtering by **release date (only past releases)** and sorting by **latest first**.

### **4️⃣ AI Matches Mood to Movies**
GPT-4o-mini analyzes **movie overviews** and finds the **top 3 best-matching** movies, along with explanations.

### **5️⃣ Display Recommendations**
The 3 best-matching movies are displayed with **titles, release dates, posters, and why they fit the user's mood**.

---

## 🔧 Setup Instructions  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/CineMood2.git
cd CineMood2
```
### **2️⃣ Set Up API Keys**
Create a `.env` file and add your OpenAI & TMDB API keys:

```bash
OPENAI_API_KEY=your_openai_api_key
TMDB_API_KEY=your_tmdb_api_key
```
### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the App**
```bash
streamlit run app.py
```

### **5️⃣ (Optional) Run with Docker**
```bash
docker-compose up --build
```

### **🧪 Running Tests**
```bash
pytest
```

---

💡 **Built with ❤️ by [Thanh Tung Vu](https://thanhtungvudata.github.io/).**  
🌟 Star this repo if you find it useful!

---

🚀 **Enjoy mood-based movie recommendations! Let me know what you think! 🎬😊**

