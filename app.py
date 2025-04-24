import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

st.set_page_config(
    page_title="AI Driven Study Partner", 
    page_icon="🤖", 
    layout="wide"
)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

st.markdown("""
<style>
    .gradient-header {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem 0.5rem 0 0;
    }
    .history-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def get_response(prompt, difficulty="intermediate"):
    difficulty_prompts = {
        "beginner": "Explain this in simple terms for a beginner: ",
        "intermediate": "Provide a detailed explanation of: ",
        "advanced": "Give an in-depth technical analysis of: "
    }
    full_prompt = f"{difficulty_prompts[difficulty]}{prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def save_to_history(question, answer):
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "question": question,
        "answer": answer
    })

with st.container():
    st.markdown('<div class="gradient-header"><h1>AI Learning Buddy</h1></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("Settings")
        difficulty = st.select_slider(
            "Select difficulty level",
            options=["beginner", "intermediate", "advanced"],
            value="intermediate",
            key="difficulty_slider"
        )

tab1, tab2, tab3, tab4 = st.tabs(["📚 Learn", "🧩 Quiz", "📝 Summarize", "📈 Review"])

# Learn Tab
with tab1:
    st.header("Learn Something New")
    user_prompt = st.text_area("What would you like to learn about?", key="learn_prompt", height=100)
    if st.button("Get Answer", key="learn_button", use_container_width=True):
        if user_prompt:
            with st.spinner("Generating response..."):
                response = get_response(user_prompt, difficulty)
                if response:
                    st.success("Here's your explanation:")
                    st.write(response)
                    save_to_history(user_prompt, response)
        else:
            st.warning("Please enter a question")

# Quiz Tab
with tab2:
    st.header("Generate Quiz")
    quiz_topic = st.text_input("Enter a topic for a quick quiz:", key="quiz_topic")

    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = []
        st.session_state.quiz_answers = {}

    if st.button("Generate Quiz", key="quiz_button", use_container_width=True):
        if quiz_topic:
            with st.spinner("Creating your quiz..."):
                quiz_prompt = f"""Create a 3-question quiz about "{quiz_topic}" suitable for {difficulty} level.
Use this exact format:
Q1: Question text
A. Option A
B. Option B
C. Option C
D. Option D
Answer: A
Ensure each question and option is on its own line exactly as above."""
                
                quiz_text = get_response(quiz_prompt, difficulty)

                # 🔍 Show raw quiz text to debug formatting
                st.text("Raw quiz text:\n" + quiz_text)

                if quiz_text:
                    st.session_state.quiz_data = []
                    st.session_state.quiz_answers = {}

                    # 🛠️ Loosened regex to match flexible formats
                    questions = re.findall(
                        r"Q\d*[:\-]?\s*(.*?)\s*A[.)]\s*(.*?)\s*B[.)]\s*(.*?)\s*C[.)]\s*(.*?)\s*D[.)]\s*(.*?)\s*Answer[:\-]?\s*([A-D])",
                        quiz_text, re.DOTALL
                    )
                    for i, (q, a, b, c, d, correct) in enumerate(questions):
                        st.session_state.quiz_data.append({
                            "question": q.strip(),
                            "options": [a.strip(), b.strip(), c.strip(), d.strip()],
                            "correct": correct.strip()
                        })

    if st.session_state.quiz_data:
        with st.form("quiz_form"):
            all_answered = True
            for idx, q in enumerate(st.session_state.quiz_data):
                st.subheader(f"Q{idx+1}: {q['question']}")
                selected = st.radio("Select one:", options=q['options'], key=f"quiz_q_{idx}", index=None)
                if selected is None:
                    all_answered = False
                st.session_state.quiz_answers[f"q{idx}"] = selected
            submitted = st.form_submit_button("Submit Quiz")
            if submitted:
                if not all_answered:
                    st.warning("Please answer all the questions before submitting.")
                else:
                    score = 0
                    total = len(st.session_state.quiz_data)
                    result_summary = []
                    for idx, q in enumerate(st.session_state.quiz_data):
                        selected = st.session_state.quiz_answers[f"q{idx}"]
                        correct_index = ord(q['correct']) - ord('A')
                        correct_option = q['options'][correct_index]
                        is_correct = (selected == correct_option)
                        if is_correct:
                            score += 1
                        result_summary.append({
                            "question": q['question'],
                            "your_answer": selected,
                            "correct_answer": correct_option,
                            "result": "✅ Correct" if is_correct else "❌ Incorrect"
                        })
                    st.success(f"Your Score: {score}/{total}")
                    st.write("### Detailed Results")
                    for res in result_summary:
                        st.markdown(f"**{res['question']}**")
                        st.markdown(f"- Your Answer: {res['your_answer']}")
                        st.markdown(f"- Correct Answer: {res['correct_answer']}")
                        st.markdown(f"- Result: {res['result']}")
                    if 'quiz_history' not in st.session_state:
                        st.session_state.quiz_history = []
                    st.session_state.quiz_history.append({
                        "topic": quiz_topic,
                        "score": f"{score}/{total}",
                        "results": result_summary
                    })

# Summarize Tab
with tab3:
    st.header("Summarize Text or Notes")
    text_to_summarize = st.text_area("Paste the text you'd like to summarize:", key="summarize_input", height=200)
    if st.button("Summarize", key="summarize_button", use_container_width=True):
        if text_to_summarize:
            with st.spinner("Generating summary..."):
                summary_prompt = f"Summarize this text: {text_to_summarize}"
                summary = get_response(summary_prompt, difficulty)
                if summary:
                    st.success("Here's the summary:")
                    st.write(summary)
                    if 'summarize_history' not in st.session_state:
                        st.session_state.summarize_history = []
                    st.session_state.summarize_history.append({
                        "input": text_to_summarize,
                        "summary": summary
                    })
        else:
            st.warning("Please paste some text to summarize")

# Review Tab
with tab4:
    st.header("Learning History")

    if 'history' in st.session_state and st.session_state.history:
        st.subheader("🧠 Learn History")
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Topic {i+1}", expanded=False):
                st.markdown(f"""
                <div class="history-card">
                    <h4>Question:</h4>
                    <p>{item['question']}</p>
                    <h4>Answer:</h4>
                    <p>{item['answer']}</p>
                </div>
                """, unsafe_allow_html=True)

    if 'summarize_history' in st.session_state and st.session_state.summarize_history:
        st.subheader("📝 Summarization History")
        for i, item in enumerate(st.session_state.summarize_history):
            with st.expander(f"Summary {i+1}", expanded=False):
                st.markdown(f"""
                <div class="history-card">
                    <h4>Original Text:</h4>
                    <p>{item['input']}</p>
                    <h4>Summary:</h4>
                    <p>{item['summary']}</p>
                </div>
                """, unsafe_allow_html=True)

    if 'quiz_history' in st.session_state and st.session_state.quiz_history:
        st.subheader("🧩 Quiz History")
        for i, qh in enumerate(st.session_state.quiz_history):
            with st.expander(f"Quiz {i+1} - Topic: {qh['topic']} | Score: {qh['score']}", expanded=False):
                for res in qh['results']:
                    st.markdown(f"""
                    <div class="history-card">
                        <h4>{res['question']}</h4>
                        <p>Your Answer: {res['your_answer']}<br>
                        Correct Answer: {res['correct_answer']}<br>
                        Result: {res['result']}</p>
                    </div>
                    """, unsafe_allow_html=True)

    if st.button("Clear History", key="clear_history", use_container_width=True):
        st.session_state.history = []
        st.session_state.summarize_history = []
        st.session_state.quiz_history = []
        st.success("History cleared successfully!")
