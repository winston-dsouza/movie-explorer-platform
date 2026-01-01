import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from app.core.database import SessionLocal, engine, Base
from app.models.models import Movie, Actor, Director, Genre, Review

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        genre_count = db.query(Genre).count()
        print(f"Current genre count: {genre_count}")
        if genre_count > 0:
            print("Database already seeded. Skipping...")
            return
        
        print("Starting database seeding...")
        
        # Create Genres
        genres = [
            Genre(name="Action", description="High-energy films with physical stunts and chases"),
            Genre(name="Comedy", description="Films designed to make audiences laugh"),
            Genre(name="Drama", description="Serious, plot-driven films with realistic characters"),
            Genre(name="Science Fiction", description="Films with futuristic or scientific elements"),
            Genre(name="Horror", description="Films designed to frighten and invoke fear"),
            Genre(name="Romance", description="Films centered on romantic relationships"),
            Genre(name="Thriller", description="Suspenseful films with high tension"),
            Genre(name="Animation", description="Films created using animation techniques"),
            Genre(name="Adventure", description="Exciting films with exploration and journeys"),
            Genre(name="Fantasy", description="Films with magical and supernatural elements")
        ]
        db.add_all(genres)
        db.commit()
        
        # Create Directors
        directors = [
            Director(name="Christopher Nolan", bio="British-American filmmaker known for complex narratives", 
                    birth_date=date(1970, 7, 30), nationality="British-American"),
            Director(name="Steven Spielberg", bio="American filmmaker and pioneer of the New Hollywood era", 
                    birth_date=date(1946, 12, 18), nationality="American"),
            Director(name="Quentin Tarantino", bio="American filmmaker known for stylized violence and dialogue", 
                    birth_date=date(1963, 3, 27), nationality="American"),
            Director(name="Martin Scorsese", bio="American filmmaker known for crime films", 
                    birth_date=date(1942, 11, 17), nationality="American"),
            Director(name="Greta Gerwig", bio="American filmmaker and actress", 
                    birth_date=date(1983, 8, 4), nationality="American"),
            Director(name="Denis Villeneuve", bio="Canadian filmmaker known for sci-fi epics", 
                    birth_date=date(1967, 10, 3), nationality="Canadian")
        ]
        db.add_all(directors)
        db.commit()
        
        # Create Actors
        actors = [
            Actor(name="Leonardo DiCaprio", bio="American actor and film producer", 
                 birth_date=date(1974, 11, 11), nationality="American"),
            Actor(name="Scarlett Johansson", bio="American actress and singer", 
                 birth_date=date(1984, 11, 22), nationality="American"),
            Actor(name="Christian Bale", bio="English actor known for method acting", 
                 birth_date=date(1974, 1, 30), nationality="British"),
            Actor(name="Margot Robbie", bio="Australian actress and producer", 
                 birth_date=date(1990, 7, 2), nationality="Australian"),
            Actor(name="Tom Hanks", bio="American actor and filmmaker", 
                 birth_date=date(1956, 7, 9), nationality="American"),
            Actor(name="Meryl Streep", bio="American actress often described as the best of her generation", 
                 birth_date=date(1949, 6, 22), nationality="American"),
            Actor(name="Robert Downey Jr.", bio="American actor known for Iron Man", 
                 birth_date=date(1965, 4, 4), nationality="American"),
            Actor(name="Ryan Gosling", bio="Canadian actor and musician", 
                 birth_date=date(1980, 11, 12), nationality="Canadian"),
            Actor(name="Emma Stone", bio="American actress", 
                 birth_date=date(1988, 11, 6), nationality="American"),
            Actor(name="Brad Pitt", bio="American actor and film producer", 
                 birth_date=date(1963, 12, 18), nationality="American")
        ]
        db.add_all(actors)
        db.commit()
        
        # Create Movies
        movies_data = [
            {
                "title": "Inception",
                "release_year": 2010,
                "description": "A thief who steals corporate secrets through dream-sharing technology.",
                "rating": 8.8,
                "runtime_minutes": 148,
                "director": directors[0],  # Christopher Nolan
                "genres": [genres[0], genres[3], genres[6]],  # Action, Sci-Fi, Thriller
                "actors": [actors[0], actors[7], actors[8]]  # DiCaprio, Gosling, Stone
            },
            {
                "title": "The Dark Knight",
                "release_year": 2008,
                "description": "Batman battles the Joker's reign of chaos and terror in Gotham City.",
                "rating": 9.0,
                "runtime_minutes": 152,
                "director": directors[0],  # Christopher Nolan
                "genres": [genres[0], genres[2], genres[6]],  # Action, Drama, Thriller
                "actors": [actors[2]]  # Christian Bale
            },
            {
                "title": "Pulp Fiction",
                "release_year": 1994,
                "description": "Various interconnected stories of crime in Los Angeles.",
                "rating": 8.9,
                "runtime_minutes": 154,
                "director": directors[2],  # Tarantino
                "genres": [genres[2], genres[6]],  # Drama, Thriller
                "actors": []
            },
            {
                "title": "Barbie",
                "release_year": 2023,
                "description": "Barbie and Ken are having the time of their lives in Colorful Barbieland.",
                "rating": 7.0,
                "runtime_minutes": 114,
                "director": directors[4],  # Greta Gerwig
                "genres": [genres[1], genres[8], genres[9]],  # Comedy, Adventure, Fantasy
                "actors": [actors[3], actors[7]]  # Margot Robbie, Ryan Gosling
            },
            {
                "title": "Dune",
                "release_year": 2021,
                "description": "A noble family becomes embroiled in a war for the desert planet Arrakis.",
                "rating": 8.0,
                "runtime_minutes": 155,
                "director": directors[5],  # Denis Villeneuve
                "genres": [genres[3], genres[8]],  # Sci-Fi, Adventure
                "actors": []
            },
            {
                "title": "Saving Private Ryan",
                "release_year": 1998,
                "description": "Following the Normandy Landings, a group searches for a paratrooper.",
                "rating": 8.6,
                "runtime_minutes": 169,
                "director": directors[1],  # Spielberg
                "genres": [genres[0], genres[2]],  # Action, Drama
                "actors": [actors[4]]  # Tom Hanks
            },
            {
                "title": "The Wolf of Wall Street",
                "release_year": 2013,
                "description": "Based on the true story of Jordan Belfort's rise and fall.",
                "rating": 8.2,
                "runtime_minutes": 180,
                "director": directors[3],  # Scorsese
                "genres": [genres[1], genres[2]],  # Comedy, Drama
                "actors": [actors[0], actors[3]]  # DiCaprio, Margot Robbie
            }
        ]
        
        for movie_data in movies_data:
            movie = Movie(
                title=movie_data["title"],
                release_year=movie_data["release_year"],
                description=movie_data["description"],
                rating=movie_data["rating"],
                runtime_minutes=movie_data["runtime_minutes"],
                director=movie_data["director"]
            )
            movie.genres = movie_data["genres"]
            movie.actors = movie_data["actors"]
            db.add(movie)
        
        db.commit()
        
        # Add some reviews
        movies = db.query(Movie).all()
        reviews = [
            Review(
                movie_id=movies[0].id,
                reviewer_name="John Doe",
                rating=9.0,
                comment="Mind-bending masterpiece! Nolan at his best.",
                created_at=date(2023, 1, 15)
            ),
            Review(
                movie_id=movies[0].id,
                reviewer_name="Jane Smith",
                rating=8.5,
                comment="Complex but rewarding. Multiple viewings recommended.",
                created_at=date(2023, 2, 20)
            ),
            Review(
                movie_id=movies[1].id,
                reviewer_name="Movie Critic",
                rating=10.0,
                comment="Heath Ledger's Joker is legendary!",
                created_at=date(2023, 3, 10)
            ),
            Review(
                movie_id=movies[3].id,
                reviewer_name="Pink Fan",
                rating=7.5,
                comment="Surprisingly deep and entertaining!",
                created_at=date(2023, 8, 1)
            )
        ]
        db.add_all(reviews)
        db.commit()
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
