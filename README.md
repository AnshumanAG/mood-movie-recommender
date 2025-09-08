# 🎬 Mood Movie Recommender

A **Netflix-like recommendation system** that provides **mood-based movie suggestions** using **NLP + hybrid recommendation algorithms**.

## 🚀 Features
- Mood-based recommendations (funny, romantic, short, thrilling)
- Hybrid engine (content + collaborative filtering)
- FastAPI backend + Streamlit UI
- Authentication & user profiles

## 🛠 Tech Stack
- Python, FastAPI, Scikit-learn, Pandas, SQLAlchemy
- NLP (VADER, TF-IDF)
- Frontend: HTML, Tailwind, Streamlit

## 📊 How to Run

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn main:app --reload

# Run frontend
streamlit run app.py
