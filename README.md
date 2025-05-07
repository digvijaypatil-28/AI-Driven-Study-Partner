# 🤖 AI Driven Study Partner

An interactive, AI-powered educational web app built with Streamlit and Gemini API (Gemini 2.0 Flash). It helps students learn, test knowledge with quizzes, summarize content, and review their learning history — all in one place.

---

## 🚀 Features

### 📚 Learn
- Ask questions on any topic.
- Choose difficulty level: Beginner, Intermediate, Advanced.
- Get tailored, human-friendly responses.

### 🧩 Quiz
- Generate a 10-question MCQ quiz on any topic.
- Select your answers and get a detailed score.
- Review correct vs. incorrect responses.

### 📝 Summarize
- Paste notes, articles, or paragraphs.
- Get concise summaries at selected difficulty levels.

### 📈 Review
- View history of your learning, quizzes, and summaries.
- Expandable cards for clean UI.
- Option to clear history.

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **AI Backend:** Google Gemini API (gemini-2.0-flash-exp)
- **Environment Variables:** `dotenv`
- **Regex:** For parsing quiz responses
- **Python Version:** 3.8+

---

## 🧩 Requirements

Install dependencies using pip:

```bash
pip install streamlit python-dotenv google-generativeai

🔐 Setup Instructions
1.Clone this repository:
git clone https://github.com/your-username/ai-driven-study-partner.git
cd ai-driven-study-partner

2.Set your Gemini API Key:

Create a .env file in the root directory:
GEMINI_API_KEY=your_gemini_api_key_here

3.Run the Streamlit app:
streamlit run app.py

📁 Folder Structure
bash
Copy
Edit
ai-driven-study-partner/
├── .env
├── app.py
├── README.md
└── requirements.txt

🧠 Tips
Use "Beginner" mode if you're just starting with a topic.

Summaries are helpful for quick reviews before exams.

Your session history is saved temporarily—don't forget to copy notes before you leave.

📜 License
MIT License © 2025 Digvijay Patil

🙋‍♂️ Maintained By
Digvijay – Engineering Student and AI Enthusiast

