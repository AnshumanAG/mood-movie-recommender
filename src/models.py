from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    mood_entries = relationship("MoodEntry", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    genre = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String(100), nullable=False)
    cast = Column(Text, nullable=True)
    plot = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    mood_tags = Column(Text, nullable=True)  # JSON string of mood associations
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    recommendations = relationship("Recommendation", back_populates="movie")

class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood_text = Column(Text, nullable=False)
    detected_mood = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="mood_entries")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    recommendation_score = Column(Float, nullable=False)
    mood_context = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_viewed = Column(Boolean, default=False)
    user_rating = Column(Integer, nullable=True)  # 1-5 star rating
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    movie = relationship("Movie", back_populates="recommendations")

# Pydantic Models for API
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int
    director: str
    cast: Optional[str] = None
    plot: Optional[str] = None
    rating: Optional[float] = None
    mood_tags: Optional[str] = None
    
    class Config:
        from_attributes = True

class MoodAnalysisRequest(BaseModel):
    mood_text: str

class MoodAnalysisResponse(BaseModel):
    detected_mood: str
    confidence_score: float
    mood_breakdown: dict

class RecommendationRequest(BaseModel):
    mood_text: Optional[str] = None
    mood_category: Optional[str] = None
    limit: int = 10

class RecommendationResponse(BaseModel):
    movie: MovieResponse
    recommendation_score: float
    mood_context: str
    reason: str

class MovieRatingRequest(BaseModel):
    movie_id: int
    rating: int  # 1-5

class Token(BaseModel):
    access_token: str
    token_type: str




