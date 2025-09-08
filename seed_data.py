#!/usr/bin/env python3
"""
Data seeding script for the Mood Movie Recommender application.
This script populates the database with sample movies and creates initial data.
"""

import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import Movie, User
from app.auth import get_password_hash
import random

def create_sample_movies():
    """Create sample movies with diverse genres and moods"""
    
    sample_movies = [
        # Happy/Comedy Movies
        {"title": "The Grand Budapest Hotel", "genre": "Comedy", "year": 2014, "director": "Wes Anderson", 
         "cast": "Ralph Fiennes, F. Murray Abraham, Mathieu Amalric", 
         "plot": "The adventures of Gustave H, a legendary concierge at a famous European hotel, and his protégé Zero Moustafa.", 
         "rating": 8.1, "mood_tags": "happy,whimsical,charming"},
        
        {"title": "Deadpool", "genre": "Action Comedy", "year": 2016, "director": "Tim Miller", 
         "cast": "Ryan Reynolds, Morena Baccarin, T.J. Miller", 
         "plot": "A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks.", 
         "rating": 8.0, "mood_tags": "happy,energetic,funny"},
        
        {"title": "La La Land", "genre": "Musical Romance", "year": 2016, "director": "Damien Chazelle", 
         "cast": "Ryan Gosling, Emma Stone, John Legend", 
         "plot": "A jazz pianist and an aspiring actress fall in love while pursuing their dreams in Los Angeles.", 
         "rating": 8.0, "mood_tags": "happy,romantic,energetic"},
        
        # Sad/Drama Movies
        {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "director": "Frank Darabont", 
         "cast": "Tim Robbins, Morgan Freeman, Bob Gunton", 
         "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", 
         "rating": 9.3, "mood_tags": "sad,hopeful,inspiring"},
        
        {"title": "Forrest Gump", "genre": "Drama Romance", "year": 1994, "director": "Robert Zemeckis", 
         "cast": "Tom Hanks, Robin Wright, Gary Sinise", 
         "plot": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.", 
         "rating": 8.8, "mood_tags": "sad,hopeful,touching"},
        
        {"title": "The Green Mile", "genre": "Drama Fantasy", "year": 1999, "director": "Frank Darabont", 
         "cast": "Tom Hanks, Michael Clarke Duncan, David Morse", 
         "plot": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.", 
         "rating": 8.6, "mood_tags": "sad,emotional,thoughtful"},
        
        # Angry/Action Movies
        {"title": "Mad Max: Fury Road", "genre": "Action Adventure", "year": 2015, "director": "George Miller", 
         "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult", 
         "plot": "In a post-apocalyptic wasteland, Max teams up with a mysterious woman to escape from a tyrannical warlord.", 
         "rating": 8.1, "mood_tags": "angry,energetic,adventurous"},
        
        {"title": "John Wick", "genre": "Action Thriller", "year": 2014, "director": "Chad Stahelski", 
         "cast": "Keanu Reeves, Michael Nyqvist, Alfie Allen", 
         "plot": "An ex-hit-man comes out of retirement to track down the gangsters that took everything from him.", 
         "rating": 7.4, "mood_tags": "angry,energetic,revenge"},
        
        {"title": "The Dark Knight", "genre": "Action Crime", "year": 2008, "director": "Christopher Nolan", 
         "cast": "Christian Bale, Heath Ledger, Aaron Eckhart", 
         "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", 
         "rating": 9.0, "mood_tags": "angry,dark,intense"},
        
        # Calm/Drama Movies
        {"title": "Lost in Translation", "genre": "Drama Romance", "year": 2003, "director": "Sofia Coppola", 
         "cast": "Bill Murray, Scarlett Johansson, Giovanni Ribisi", 
         "plot": "A faded movie star and a neglected young woman form an unlikely bond after crossing paths in Tokyo.", 
         "rating": 7.7, "mood_tags": "calm,contemplative,peaceful"},
        
        {"title": "Her", "genre": "Drama Romance Sci-Fi", "year": 2013, "director": "Spike Jonze", 
         "cast": "Joaquin Phoenix, Amy Adams, Scarlett Johansson", 
         "plot": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.", 
         "rating": 8.0, "mood_tags": "calm,romantic,thoughtful"},
        
        {"title": "The Secret Life of Walter Mitty", "genre": "Adventure Comedy Drama", "year": 2013, "director": "Ben Stiller", 
         "cast": "Ben Stiller, Kristen Wiig, Jon Daly", 
         "plot": "When his job along with that of his co-worker are threatened, Walter takes action in the real world embarking on a global journey that turns into an adventure more extraordinary than anything he could have ever imagined.", 
         "rating": 7.3, "mood_tags": "calm,adventurous,inspiring"},
        
        # Energetic/Action Movies
        {"title": "Top Gun: Maverick", "genre": "Action Drama", "year": 2022, "director": "Joseph Kosinski", 
         "cast": "Tom Cruise, Miles Teller, Jennifer Connelly", 
         "plot": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it.", 
         "rating": 8.3, "mood_tags": "energetic,adventurous,exciting"},
        
        {"title": "Baby Driver", "genre": "Action Crime", "year": 2017, "director": "Edgar Wright", 
         "cast": "Ansel Elgort, Jon Bernthal, Jon Hamm", 
         "plot": "After being coerced into working for a crime boss, a young getaway driver finds himself taking part in a heist doomed to fail.", 
         "rating": 7.6, "mood_tags": "energetic,exciting,stylish"},
        
        {"title": "Spider-Man: Into the Spider-Verse", "genre": "Animation Action", "year": 2018, "director": "Bob Persichetti", 
         "cast": "Shameik Moore, Jake Johnson, Hailee Steinfeld", 
         "plot": "Teen Miles Morales becomes Spider-Man of his reality, crossing his path with five counterparts from other dimensions to stop a threat for all realities.", 
         "rating": 8.4, "mood_tags": "energetic,exciting,inspiring"},
        
        # Romantic Movies
        {"title": "The Notebook", "genre": "Romance Drama", "year": 2004, "director": "Nick Cassavetes", 
         "cast": "Ryan Gosling, Rachel McAdams, James Garner", 
         "plot": "A poor yet passionate young man falls in love with a rich young woman, giving her a sense of freedom, but they are soon separated because of their social differences.", 
         "rating": 7.8, "mood_tags": "romantic,emotional,touching"},
        
        {"title": "Casablanca", "genre": "Drama Romance", "year": 1942, "director": "Michael Curtiz", 
         "cast": "Humphrey Bogart, Ingrid Bergman, Paul Henreid", 
         "plot": "A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco.", 
         "rating": 8.5, "mood_tags": "romantic,classic,timeless"},
        
        {"title": "Before Sunrise", "genre": "Drama Romance", "year": 1995, "director": "Richard Linklater", 
         "cast": "Ethan Hawke, Julie Delpy, Andrea Eckert", 
         "plot": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. Unfortunately, both know that this will probably be their only night together.", 
         "rating": 8.1, "mood_tags": "romantic,contemplative,beautiful"},
        
        # Anxious/Thriller Movies
        {"title": "Gone Girl", "genre": "Drama Mystery Thriller", "year": 2014, "director": "David Fincher", 
         "cast": "Ben Affleck, Rosamund Pike, Neil Patrick Harris", 
         "plot": "With his wife's disappearance having become the focus of the media, a man sees the spotlight turned on him when it's suspected that he may not be innocent.", 
         "rating": 8.1, "mood_tags": "anxious,thrilling,psychological"},
        
        {"title": "The Silence of the Lambs", "genre": "Crime Drama Thriller", "year": 1991, "director": "Jonathan Demme", 
         "cast": "Jodie Foster, Anthony Hopkins, Scott Glenn", 
         "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", 
         "rating": 8.6, "mood_tags": "anxious,thrilling,psychological"},
        
        {"title": "Prisoners", "genre": "Crime Drama Mystery", "year": 2013, "director": "Denis Villeneuve", 
         "cast": "Hugh Jackman, Jake Gyllenhaal, Viola Davis", 
         "plot": "When Keller Dover's daughter and her friend go missing, he takes matters into his own hands as the police pursue multiple leads and the pressure mounts.", 
         "rating": 8.1, "mood_tags": "anxious,tense,emotional"},
        
        # Adventurous Movies
        {"title": "Indiana Jones and the Raiders of the Lost Ark", "genre": "Action Adventure", "year": 1981, "director": "Steven Spielberg", 
         "cast": "Harrison Ford, Karen Allen, Paul Freeman", 
         "plot": "In 1936, archaeologist and adventurer Indiana Jones is hired by the U.S. government to find the Ark of the Covenant before Adolf Hitler's Nazis can obtain its awesome powers.", 
         "rating": 8.4, "mood_tags": "adventurous,exciting,classic"},
        
        {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Adventure Drama Fantasy", "year": 2001, "director": "Peter Jackson", 
         "cast": "Elijah Wood, Ian McKellen, Orlando Bloom", 
         "plot": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.", 
         "rating": 8.8, "mood_tags": "adventurous,epic,fantasy"},
        
        {"title": "Interstellar", "genre": "Adventure Drama Sci-Fi", "year": 2014, "director": "Christopher Nolan", 
         "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain", 
         "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", 
         "rating": 8.6, "mood_tags": "adventurous,thoughtful,epic"},
        
        # Additional diverse movies
        {"title": "Parasite", "genre": "Comedy Drama Thriller", "year": 2019, "director": "Bong Joon Ho", 
         "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong", 
         "plot": "A poor family schemes to become employed by a wealthy family and infiltrate their household by posing as unrelated, highly qualified individuals.", 
         "rating": 8.5, "mood_tags": "thoughtful,social,thrilling"},
        
        {"title": "Get Out", "genre": "Horror Mystery Thriller", "year": 2017, "director": "Jordan Peele", 
         "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford", 
         "plot": "A young African-American visits his white girlfriend's parents for the weekend, where his uneasiness about their reception of him eventually reaches a boiling point.", 
         "rating": 7.7, "mood_tags": "anxious,thoughtful,thrilling"},
        
        {"title": "Whiplash", "genre": "Drama Music", "year": 2014, "director": "Damien Chazelle", 
         "cast": "Miles Teller, J.K. Simmons, Melissa Benoist", 
         "plot": "A promising young drummer enrolls at a cut-throat music conservatory where he falls under the wing of an instructor who will stop at nothing to realize a student's potential.", 
         "rating": 8.5, "mood_tags": "intense,passionate,driven"},
        
        {"title": "Moonlight", "genre": "Drama", "year": 2016, "director": "Barry Jenkins", 
         "cast": "Mahershala Ali, Naomie Harris, Trevante Rhodes", 
         "plot": "A young African-American man grapples with his identity and sexuality while experiencing the everyday struggles of childhood, adolescence, and burgeoning adulthood.", 
         "rating": 7.4, "mood_tags": "contemplative,emotional,beautiful"},
        
        {"title": "The Shape of Water", "genre": "Drama Fantasy Romance", "year": 2017, "director": "Guillermo del Toro", 
         "cast": "Sally Hawkins, Michael Shannon, Richard Jenkins", 
         "plot": "At a top secret research facility in the 1960s, a lonely janitor forms a unique relationship with an amphibious creature that is being held in captivity.", 
         "rating": 7.3, "mood_tags": "romantic,fantasy,beautiful"},
        
        {"title": "Blade Runner 2049", "genre": "Drama Mystery Sci-Fi", "year": 2017, "director": "Denis Villeneuve", 
         "cast": "Ryan Gosling, Harrison Ford, Ana de Armas", 
         "plot": "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who's been missing for thirty years.", 
         "rating": 8.0, "mood_tags": "contemplative,atmospheric,thoughtful"},
        
        {"title": "Dune", "genre": "Adventure Drama Sci-Fi", "year": 2021, "director": "Denis Villeneuve", 
         "cast": "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac", 
         "plot": "Feature adaptation of Frank Herbert's science fiction novel, about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.", 
         "rating": 8.0, "mood_tags": "epic,adventurous,thoughtful"},
        
        {"title": "Everything Everywhere All at Once", "genre": "Action Adventure Comedy", "year": 2022, "director": "Daniel Kwan", 
         "cast": "Michelle Yeoh, Stephanie Hsu, Ke Huy Quan", 
         "plot": "A Chinese-American laundromat owner is swept up in an insane adventure in which she alone can save existence by exploring other universes and connecting with the lives she could have led.", 
         "rating": 8.1, "mood_tags": "energetic,creative,thoughtful"},
        
        {"title": "The Batman", "genre": "Action Crime Drama", "year": 2022, "director": "Matt Reeves", 
         "cast": "Robert Pattinson, Zoë Kravitz, Paul Dano", 
         "plot": "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement.", 
         "rating": 7.8, "mood_tags": "dark,atmospheric,thrilling"},
    ]
    
    return sample_movies

def create_sample_user():
    """Create a sample user for testing"""
    return {
        "username": "demo_user",
        "email": "demo@example.com",
        "password": "demo123"
    }

def seed_database():
    """Main function to seed the database"""
    print("Initializing database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if movies already exist
        existing_movies = db.query(Movie).count()
        if existing_movies > 0:
            print(f"Database already contains {existing_movies} movies. Skipping movie seeding.")
        else:
            print("Seeding movies...")
            sample_movies = create_sample_movies()
            
            for movie_data in sample_movies:
                movie = Movie(**movie_data)
                db.add(movie)
            
            db.commit()
            print(f"Successfully added {len(sample_movies)} movies to the database.")
        
        # Check if demo user exists
        existing_user = db.query(User).filter(User.username == "demo_user").first()
        if existing_user:
            print("Demo user already exists. Skipping user creation.")
        else:
            print("Creating demo user...")
            user_data = create_sample_user()
            hashed_password = get_password_hash(user_data["password"])
            
            demo_user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password
            )
            db.add(demo_user)
            db.commit()
            print("Demo user created successfully!")
            print("Username: demo_user")
            print("Password: demo123")
        
        print("\nDatabase seeding completed successfully!")
        print("\nYou can now:")
        print("1. Start the application with: python -m uvicorn app.main:app --reload")
        print("2. Visit http://localhost:8000 to use the web interface")
        print("3. Visit http://localhost:8000/docs for API documentation")
        print("4. Login with demo_user / demo123 to test the application")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()



