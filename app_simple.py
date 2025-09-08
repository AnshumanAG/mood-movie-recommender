#!/usr/bin/env python3
"""
Simplified version of the Mood Movie Recommender that works with minimal dependencies
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import random

# Simple in-memory data storage
movies_db = [
    {"id": 1, "title": "The Grand Budapest Hotel", "genre": "Comedy", "year": 2014, "director": "Wes Anderson", "rating": 8.1},
    {"id": 2, "title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "director": "Frank Darabont", "rating": 9.3},
    {"id": 3, "title": "Mad Max: Fury Road", "genre": "Action", "year": 2015, "director": "George Miller", "rating": 8.1},
    {"id": 4, "title": "Lost in Translation", "genre": "Drama", "year": 2003, "director": "Sofia Coppola", "rating": 7.7},
    {"id": 5, "title": "The Notebook", "genre": "Romance", "year": 2004, "director": "Nick Cassavetes", "rating": 7.8},
    {"id": 6, "title": "Gone Girl", "genre": "Thriller", "year": 2014, "director": "David Fincher", "rating": 8.1},
    {"id": 7, "title": "Indiana Jones", "genre": "Adventure", "year": 1981, "director": "Steven Spielberg", "rating": 8.4},
    {"id": 8, "title": "La La Land", "genre": "Musical", "year": 2016, "director": "Damien Chazelle", "rating": 8.0},
]

# Simple mood mapping
mood_genres = {
    "happy": ["Comedy", "Musical", "Animation"],
    "sad": ["Drama", "Romance"],
    "angry": ["Action", "Thriller"],
    "calm": ["Drama", "Romance"],
    "energetic": ["Action", "Adventure"],
    "romantic": ["Romance", "Drama"],
    "anxious": ["Thriller", "Mystery"],
    "adventurous": ["Adventure", "Action"]
}

app = FastAPI(title="Simple Mood Movie Recommender", version="1.0.0")

class MoodRequest(BaseModel):
    mood_text: Optional[str] = None
    mood_category: Optional[str] = None
    limit: int = 5

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int
    director: str
    rating: float

class RecommendationResponse(BaseModel):
    movie: MovieResponse
    recommendation_score: float
    mood_context: str
    reason: str

@app.get("/")
async def root():
    return {"message": "Simple Mood Movie Recommender API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/movies", response_model=List[MovieResponse])
async def get_movies():
    return movies_db

@app.post("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(request: MoodRequest):
    """Get simple movie recommendations based on mood"""
    
    # Simple mood detection
    mood = "happy"  # default
    if request.mood_category:
        mood = request.mood_category
    elif request.mood_text:
        text = request.mood_text.lower()
        if any(word in text for word in ["sad", "depressed", "down"]):
            mood = "sad"
        elif any(word in text for word in ["angry", "mad", "furious"]):
            mood = "angry"
        elif any(word in text for word in ["calm", "peaceful", "relaxed"]):
            mood = "calm"
        elif any(word in text for word in ["energetic", "excited", "pumped"]):
            mood = "energetic"
        elif any(word in text for word in ["romantic", "love", "passionate"]):
            mood = "romantic"
        elif any(word in text for word in ["anxious", "worried", "nervous"]):
            mood = "anxious"
        elif any(word in text for word in ["adventurous", "exciting", "thrilling"]):
            mood = "adventurous"
    
    # Get preferred genres for mood
    preferred_genres = mood_genres.get(mood, ["Drama", "Comedy"])
    
    # Filter movies by preferred genres
    recommended_movies = []
    for movie in movies_db:
        if movie["genre"] in preferred_genres:
            score = random.uniform(0.7, 0.95)  # Random score for demo
            recommended_movies.append({
                "movie": movie,
                "recommendation_score": score,
                "mood_context": mood,
                "reason": f"Recommended for {mood} mood based on {movie['genre']} genre"
            })
    
    # Sort by score and limit results
    recommended_movies.sort(key=lambda x: x["recommendation_score"], reverse=True)
    return recommended_movies[:request.limit]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




