# Mood Movie Recommender 🎬

A Python-powered web application that provides highly personalized, mood-based movie recommendations using machine learning, data processing, and NLP techniques.

## 🌟 Features

- **Mood Analysis**: Advanced NLP-powered mood detection from text input
- **Personalized Recommendations**: ML-based movie recommendations tailored to your emotional state
- **User Authentication**: Secure user registration and login system
- **Modern Web Interface**: Beautiful, responsive web UI built with Tailwind CSS
- **RESTful API**: Complete FastAPI backend with comprehensive endpoints
- **Database Integration**: SQLAlchemy ORM with support for multiple databases
- **Real-time Processing**: Fast mood analysis and recommendation generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mood-movie-recommender
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the root directory
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "DATABASE_URL=sqlite:///./mood_movie_recommender.db" >> .env
   ```

5. **Seed the database with sample data**
   ```bash
   python seed_data.py
   ```

6. **Start the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

7. **Access the application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## 🎯 Usage

### Web Interface

1. **Register/Login**: Create an account or use the demo credentials:
   - Username: `demo_user`
   - Password: `demo123`

2. **Describe Your Mood**: Enter how you're feeling in the text area or select a quick mood option

3. **Get Recommendations**: Click "Get Movie Recommendations" to receive personalized suggestions

4. **Rate Movies**: Provide feedback on recommendations to improve future suggestions

### API Usage

#### Authentication
```bash
# Register a new user
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "email": "your_email", "password": "your_password"}'

# Login to get access token
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=your_username&password=your_password"
```

#### Get Recommendations
```bash
# Get recommendations based on mood text
curl -X POST "http://localhost:8000/recommendations" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"mood_text": "I feel happy and energetic today!", "limit": 5}'

# Get recommendations based on mood category
curl -X POST "http://localhost:8000/recommendations" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"mood_category": "happy", "limit": 5}'
```

## 🏗️ Architecture

### Backend Components

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Pydantic**: Data validation and settings management using Python type annotations
- **JWT Authentication**: Secure token-based authentication
- **NLTK & TextBlob**: Natural language processing libraries
- **Scikit-learn**: Machine learning library for recommendation algorithms

### Frontend Components

- **HTML5/CSS3**: Modern web standards
- **Tailwind CSS**: Utility-first CSS framework
- **Vanilla JavaScript**: No framework dependencies for simplicity
- **Font Awesome**: Icon library for enhanced UI

### Machine Learning Pipeline

1. **Mood Analysis**:
   - Text preprocessing and cleaning
   - Sentiment analysis using NLTK's VADER
   - Keyword-based mood detection
   - Confidence scoring

2. **Recommendation Engine**:
   - Genre-mood mapping
   - Content-based filtering
   - User preference learning
   - Score calculation and ranking

## 📊 Database Schema

### Tables

- **users**: User accounts and authentication
- **movies**: Movie catalog with metadata
- **mood_entries**: User mood analysis history
- **recommendations**: Generated recommendations and user feedback

### Key Relationships

- Users have many mood entries and recommendations
- Movies have many recommendations
- Recommendations link users to movies with scores and context

## 🔧 Configuration

### Environment Variables

```bash
# Required
SECRET_KEY=your-secret-key-for-jwt-tokens

# Optional
DATABASE_URL=sqlite:///./mood_movie_recommender.db  # Default SQLite
ACCESS_TOKEN_EXPIRE_MINUTES=30  # JWT token expiration
```

### Database Options

- **SQLite** (default): File-based database, perfect for development
- **PostgreSQL**: Production-ready database
- **MySQL**: Alternative production database

## 🧪 Testing

### Run the application in development mode
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test the API endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get movies
curl http://localhost:8000/movies
```

## 📈 Performance & Scalability

### Current Capabilities
- Handles 1000+ movies efficiently
- Real-time mood analysis (< 1 second)
- Fast recommendation generation
- Concurrent user support

### Optimization Opportunities
- Implement caching (Redis)
- Add database indexing
- Use async database operations
- Implement recommendation pre-computation

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization
- SQL injection prevention via ORM

## 🚀 Deployment

### Docker Deployment (Recommended)

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and run**
   ```bash
   docker build -t mood-movie-recommender .
   docker run -p 8000:8000 mood-movie-recommender
   ```

### Cloud Deployment

- **Heroku**: Easy deployment with Procfile
- **AWS**: EC2, ECS, or Lambda deployment
- **Google Cloud**: App Engine or Cloud Run
- **Azure**: Container Instances or App Service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NLTK**: Natural Language Toolkit for sentiment analysis
- **FastAPI**: Modern web framework for Python APIs
- **Tailwind CSS**: Utility-first CSS framework
- **Movie data**: Curated collection of popular films

## 📞 Support

For support, email your-email@example.com or create an issue in the repository.

## 🔮 Future Enhancements

- [ ] Advanced ML models (neural networks, transformers)
- [ ] Social features (friend recommendations, sharing)
- [ ] Mobile app development
- [ ] Integration with streaming services
- [ ] Advanced user profiling
- [ ] A/B testing framework
- [ ] Real-time notifications
- [ ] Multi-language support

---

**Made with ❤️ for movie lovers everywhere!**



