# 🎬 CineMood2 - AI-Powered Mood-Based Movie Recommendations  

CineMood2 is an AI-powered movie recommendation system that suggests trending movies based on the user's mood. It leverages **GPT-4o-mini** to analyze user input, detect moods, and match them with suitable films using **TMDB API**.


## 🚀 Demo

🎭 **Try the app:** [CineMood2: AI-Agent-Assisted Mood-Based Movie Recommendation](https://huggingface.co/spaces/thanhtungvudata/cinemoodv2)  
📝 **Blog post:** [Handling Validation and Hallucination Issues in LLM for a Mood-Based Movie Recommendation App](https://thanhtungvudata.github.io/data%20science%20projects/cinemood2-issues/)
---

## 🚀 Features  
- **Mood Detection**: Extracts mood-related words from user input and validates them against a predefined list.
- **Movie Recommendation**: Fetches trending movies and ranks them based on mood compatibility.
- **New Validation Mechanisms**: Ensures user input is meaningful and prevents AI hallucinations.
- **Streamlit Interface**: User-friendly web UI for easy interaction.

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

