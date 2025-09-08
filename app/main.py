from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import os

from app.database import get_db, init_db
from app.models import (
    User, Movie, MoodEntry, Recommendation,
    UserCreate, UserResponse, MovieResponse, 
    MoodAnalysisRequest, MoodAnalysisResponse,
    RecommendationRequest, RecommendationResponse,
    MovieRatingRequest, Token
)
from app.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, get_user_by_username, get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.ml_engine import MLPipeline
from datetime import timedelta

# Initialize FastAPI app
app = FastAPI(
    title="Mood Movie Recommender",
    description="A personalized movie recommendation system based on mood analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML pipeline
ml_pipeline = MLPipeline()

# Initialize database
init_db()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>Mood Movie Recommender</title></head>
            <body>
                <h1>Mood Movie Recommender API</h1>
                <p>API is running! Visit <a href="/docs">/docs</a> for API documentation.</p>
            </body>
        </html>
        """)

@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@app.post("/analyze-mood", response_model=MoodAnalysisResponse)
async def analyze_mood(
    request: MoodAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Analyze mood from text input"""
    mood_analysis = ml_pipeline.mood_analyzer.analyze_mood(request.mood_text)
    
    # Save mood entry to database
    mood_entry = MoodEntry(
        user_id=current_user.id,
        mood_text=request.mood_text,
        detected_mood=mood_analysis['detected_mood'],
        confidence_score=mood_analysis['confidence_score']
    )
    db.add(mood_entry)
    db.commit()
    
    return MoodAnalysisResponse(
        detected_mood=mood_analysis['detected_mood'],
        confidence_score=mood_analysis['confidence_score'],
        mood_breakdown=mood_analysis['mood_breakdown']
    )

@app.post("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    request: RecommendationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get movie recommendations based on mood"""
    
    # Get movies from database
    movies = db.query(Movie).all()
    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found in database"
        )
    
    # Convert to DataFrame for ML processing
    movies_data = []
    for movie in movies:
        movies_data.append({
            'id': movie.id,
            'title': movie.title,
            'genre': movie.genre,
            'year': movie.year,
            'director': movie.director,
            'cast': movie.cast,
            'plot': movie.plot,
            'rating': movie.rating,
            'mood_tags': movie.mood_tags
        })
    
    movies_df = pd.DataFrame(movies_data)
    
    # Get user preferences (simplified for now)
    user_preferences = {
        'preferred_genres': ['drama', 'comedy', 'action']  # Could be learned from user history
    }
    
    # Process recommendation request
    if request.mood_text:
        result = ml_pipeline.process_recommendation_request(
            request.mood_text, movies_df, user_preferences, request.limit
        )
        recommendations = result['recommendations']
    elif request.mood_category:
        recommendations = ml_pipeline.recommendation_engine.get_mood_based_recommendations(
            movies_df, request.mood_category, user_preferences, request.limit
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Either mood_text or mood_category must be provided"
        )
    
    # Save recommendations to database
    recommendation_objects = []
    for rec in recommendations:
        recommendation = Recommendation(
            user_id=current_user.id,
            movie_id=rec['movie_id'],
            recommendation_score=rec['recommendation_score'],
            mood_context=rec['mood_context']
        )
        db.add(recommendation)
        recommendation_objects.append(recommendation)
    
    db.commit()
    
    # Return formatted recommendations
    response_recommendations = []
    for rec in recommendations:
        movie = next((m for m in movies if m.id == rec['movie_id']), None)
        if movie:
            response_recommendations.append(RecommendationResponse(
                movie=MovieResponse.from_orm(movie),
                recommendation_score=rec['recommendation_score'],
                mood_context=rec['mood_context'],
                reason=rec['reason']
            ))
    
    return response_recommendations

@app.post("/rate-movie")
async def rate_movie(
    request: MovieRatingRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Rate a movie recommendation"""
    
    # Find the recommendation
    recommendation = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id,
        Recommendation.movie_id == request.movie_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )
    
    # Update rating
    recommendation.user_rating = request.rating
    db.commit()
    
    return {"message": "Rating saved successfully"}

@app.get("/movies", response_model=List[MovieResponse])
async def get_movies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of movies"""
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get a specific movie by ID"""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/my-recommendations", response_model=List[RecommendationResponse])
async def get_my_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's recommendation history"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.created_at.desc()).limit(50).all()
    
    response_recommendations = []
    for rec in recommendations:
        movie = db.query(Movie).filter(Movie.id == rec.movie_id).first()
        if movie:
            response_recommendations.append(RecommendationResponse(
                movie=MovieResponse.from_orm(movie),
                recommendation_score=rec.recommendation_score,
                mood_context=rec.mood_context,
                reason=f"Previously recommended for {rec.mood_context} mood"
            ))
    
    return response_recommendations

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Mood Movie Recommender API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
