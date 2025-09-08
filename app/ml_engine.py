import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import json
from typing import Dict, List, Tuple, Optional
import logging

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt')

logger = logging.getLogger(__name__)

class MoodAnalyzer:
    """Analyzes text to detect mood and emotional state"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.mood_keywords = {
            'happy': ['happy', 'joy', 'excited', 'cheerful', 'elated', 'thrilled', 'ecstatic', 'blissful'],
            'sad': ['sad', 'depressed', 'melancholy', 'gloomy', 'down', 'blue', 'miserable', 'heartbroken'],
            'angry': ['angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated', 'livid'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'uneasy', 'apprehensive'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'zen', 'chill', 'mellow'],
            'energetic': ['energetic', 'pumped', 'motivated', 'enthusiastic', 'dynamic', 'vibrant', 'lively'],
            'romantic': ['romantic', 'love', 'passionate', 'intimate', 'sweet', 'tender', 'affectionate'],
            'adventurous': ['adventurous', 'exciting', 'thrilling', 'daring', 'bold', 'wild', 'epic']
        }
    
    def analyze_mood(self, text: str) -> Dict:
        """Analyze mood from text input"""
        if not text or not text.strip():
            return {
                'detected_mood': 'neutral',
                'confidence_score': 0.5,
                'mood_breakdown': {}
            }
        
        # Clean text
        text = self._clean_text(text)
        
        # Get sentiment scores
        sentiment_scores = self.sia.polarity_scores(text)
        
        # Analyze mood keywords
        mood_scores = self._analyze_mood_keywords(text)
        
        # Combine sentiment and mood analysis
        combined_scores = self._combine_scores(sentiment_scores, mood_scores)
        
        # Determine primary mood
        primary_mood = max(combined_scores, key=combined_scores.get)
        confidence = combined_scores[primary_mood]
        
        return {
            'detected_mood': primary_mood,
            'confidence_score': confidence,
            'mood_breakdown': combined_scores
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def _analyze_mood_keywords(self, text: str) -> Dict[str, float]:
        """Analyze mood based on keyword presence"""
        mood_scores = {mood: 0.0 for mood in self.mood_keywords.keys()}
        
        words = text.split()
        total_words = len(words)
        
        if total_words == 0:
            return mood_scores
        
        for mood, keywords in self.mood_keywords.items():
            keyword_count = sum(1 for word in words if word in keywords)
            mood_scores[mood] = keyword_count / total_words
        
        return mood_scores
    
    def _combine_scores(self, sentiment_scores: Dict, mood_scores: Dict) -> Dict[str, float]:
        """Combine sentiment and mood keyword scores"""
        combined = {}
        
        # Map sentiment to mood categories
        sentiment_mapping = {
            'positive': ['happy', 'energetic', 'romantic'],
            'negative': ['sad', 'angry', 'anxious'],
            'neutral': ['calm']
        }
        
        for mood in self.mood_keywords.keys():
            # Start with keyword-based score
            score = mood_scores.get(mood, 0.0)
            
            # Add sentiment influence
            if mood in sentiment_mapping.get('positive', []):
                score += sentiment_scores['pos'] * 0.3
            elif mood in sentiment_mapping.get('negative', []):
                score += sentiment_scores['neg'] * 0.3
            elif mood in sentiment_mapping.get('neutral', []):
                score += sentiment_scores['neu'] * 0.3
            
            # Normalize score
            combined[mood] = min(score, 1.0)
        
        # Add neutral mood if no strong mood detected
        if max(combined.values()) < 0.3:
            combined['neutral'] = 0.5
        
        return combined

class MovieRecommendationEngine:
    """Machine learning engine for movie recommendations based on mood"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.mood_movie_mapping = {
            'happy': ['comedy', 'family', 'musical', 'animation'],
            'sad': ['drama', 'romance', 'biography'],
            'angry': ['action', 'thriller', 'crime'],
            'anxious': ['drama', 'mystery', 'thriller'],
            'calm': ['drama', 'documentary', 'romance'],
            'energetic': ['action', 'adventure', 'sport'],
            'romantic': ['romance', 'drama', 'comedy'],
            'adventurous': ['adventure', 'action', 'fantasy', 'sci-fi'],
            'neutral': ['drama', 'comedy', 'thriller']
        }
    
    def get_mood_based_recommendations(self, movies_df: pd.DataFrame, mood: str, 
                                     user_preferences: Optional[Dict] = None, 
                                     limit: int = 10) -> List[Dict]:
        """Get movie recommendations based on mood"""
        
        if movies_df.empty:
            return []
        
        # Filter movies by mood-appropriate genres
        preferred_genres = self.mood_movie_mapping.get(mood, ['drama', 'comedy'])
        
        # Create genre filter
        genre_filter = movies_df['genre'].str.lower().str.contains('|'.join(preferred_genres), na=False)
        mood_movies = movies_df[genre_filter].copy()
        
        if mood_movies.empty:
            # Fallback to all movies if no mood-specific movies found
            mood_movies = movies_df.copy()
        
        # Calculate recommendation scores
        recommendations = []
        
        for _, movie in mood_movies.iterrows():
            score = self._calculate_movie_score(movie, mood, user_preferences)
            recommendations.append({
                'movie_id': movie['id'],
                'title': movie['title'],
                'genre': movie['genre'],
                'year': movie['year'],
                'director': movie['director'],
                'rating': movie.get('rating', 0),
                'recommendation_score': score,
                'mood_context': mood,
                'reason': f"Recommended for {mood} mood based on {movie['genre']} genre"
            })
        
        # Sort by recommendation score and return top results
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations[:limit]
    
    def _calculate_movie_score(self, movie: pd.Series, mood: str, 
                             user_preferences: Optional[Dict] = None) -> float:
        """Calculate recommendation score for a movie"""
        base_score = 0.5
        
        # Genre-mood alignment score
        preferred_genres = self.mood_movie_mapping.get(mood, [])
        movie_genre = movie['genre'].lower()
        
        genre_score = 0.0
        for genre in preferred_genres:
            if genre in movie_genre:
                genre_score = 0.4
                break
        
        # Rating score (if available)
        rating_score = 0.0
        if pd.notna(movie.get('rating')) and movie['rating'] > 0:
            rating_score = (movie['rating'] / 10.0) * 0.3
        
        # User preference score (if available)
        preference_score = 0.0
        if user_preferences:
            # Check if user has rated similar movies highly
            if 'preferred_genres' in user_preferences:
                for pref_genre in user_preferences['preferred_genres']:
                    if pref_genre.lower() in movie_genre:
                        preference_score = 0.2
                        break
        
        # Combine scores
        total_score = base_score + genre_score + rating_score + preference_score
        
        # Add some randomness to avoid identical scores
        total_score += np.random.normal(0, 0.05)
        
        return min(max(total_score, 0.0), 1.0)
    
    def get_similar_movies(self, movies_df: pd.DataFrame, movie_id: int, limit: int = 5) -> List[Dict]:
        """Get movies similar to a given movie using content-based filtering"""
        
        if movies_df.empty:
            return []
        
        # Find the target movie
        target_movie = movies_df[movies_df['id'] == movie_id]
        if target_movie.empty:
            return []
        
        target_movie = target_movie.iloc[0]
        
        # Create feature vectors for movies
        movie_features = []
        movie_ids = []
        
        for _, movie in movies_df.iterrows():
            # Combine title, genre, and plot for feature vector
            features = f"{movie['title']} {movie['genre']} {movie.get('plot', '')}"
            movie_features.append(features)
            movie_ids.append(movie['id'])
        
        # Vectorize movie features
        try:
            feature_matrix = self.vectorizer.fit_transform(movie_features)
            
            # Find target movie index
            target_idx = movie_ids.index(movie_id)
            
            # Calculate similarities
            similarities = cosine_similarity(feature_matrix[target_idx:target_idx+1], feature_matrix).flatten()
            
            # Get top similar movies (excluding the target movie itself)
            similar_indices = np.argsort(similarities)[::-1][1:limit+1]
            
            similar_movies = []
            for idx in similar_indices:
                if similarities[idx] > 0.1:  # Only include movies with meaningful similarity
                    movie = movies_df[movies_df['id'] == movie_ids[idx]].iloc[0]
                    similar_movies.append({
                        'movie_id': movie['id'],
                        'title': movie['title'],
                        'genre': movie['genre'],
                        'year': movie['year'],
                        'director': movie['director'],
                        'rating': movie.get('rating', 0),
                        'similarity_score': similarities[idx],
                        'reason': f"Similar to {target_movie['title']} based on content"
                    })
            
            return similar_movies
            
        except Exception as e:
            logger.error(f"Error in get_similar_movies: {e}")
            return []

class MLPipeline:
    """Main ML pipeline that combines mood analysis and recommendation"""
    
    def __init__(self):
        self.mood_analyzer = MoodAnalyzer()
        self.recommendation_engine = MovieRecommendationEngine()
    
    def process_recommendation_request(self, mood_text: str, movies_df: pd.DataFrame, 
                                    user_preferences: Optional[Dict] = None, 
                                    limit: int = 10) -> Dict:
        """Process a complete recommendation request"""
        
        # Analyze mood from text
        mood_analysis = self.mood_analyzer.analyze_mood(mood_text)
        
        # Get recommendations based on detected mood
        recommendations = self.recommendation_engine.get_mood_based_recommendations(
            movies_df, mood_analysis['detected_mood'], user_preferences, limit
        )
        
        return {
            'mood_analysis': mood_analysis,
            'recommendations': recommendations,
            'total_recommendations': len(recommendations)
        }



