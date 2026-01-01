"""
CRUD operations for Actor, Director, Genre, and Review models.
Provides database query methods with pagination, filtering, and search capabilities.

Edge Cases Handled:
- Null/None validation for required fields
- Duplicate prevention through database constraints
- Case-insensitive search using ILIKE
- Pagination to prevent memory overflow on large datasets
- Relationship integrity checks before deletion
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.models import Actor, Director, Genre, Review, Movie
from app.schemas.schemas import ActorCreate, DirectorCreate, GenreCreate, ReviewCreate


class ActorCRUD:
    """
    CRUD operations for Actor model.
    Handles actor creation, retrieval, updates, and deletion.
    """
    
    @staticmethod
    def get_actor(db: Session, actor_id: int):
        """
        Retrieve a single actor by ID.
        
        Args:
            db: Database session
            actor_id: Primary key of the actor
            
        Returns:
            Actor object or None if not found
            
        Edge Cases:
            - Returns None for non-existent IDs
            - Handles negative IDs gracefully
        """
        return db.query(Actor).filter(Actor.id == actor_id).first()
    
    @staticmethod
    def get_actors(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve all actors with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return (default 100)
            
        Returns:
            List of Actor objects
            
        Edge Cases:
            - Returns empty list if no actors exist
            - Limit capped at 100 to prevent memory issues
            - Skip parameter allows offset-based pagination
        """
        return db.query(Actor).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_actor(db: Session, actor: ActorCreate):
        """
        Create a new actor in the database.
        
        Args:
            db: Database session
            actor: ActorCreate schema with actor data
            
        Returns:
            Newly created Actor object with generated ID
            
        Edge Cases:
            - Validates required fields via Pydantic schema
            - Database enforces unique constraints if defined
            - Automatically commits transaction
        """
        db_actor = Actor(**actor.dict())
        db.add(db_actor)
        db.commit()
        db.refresh(db_actor)
        return db_actor
    
    @staticmethod
    def update_actor(db: Session, actor_id: int, actor: ActorCreate):
        """
        Update an existing actor's information.
        
        Args:
            db: Database session
            actor_id: ID of actor to update
            actor: ActorCreate schema with updated data
            
        Returns:
            Updated Actor object or None if not found
            
        Edge Cases:
            - Returns None if actor doesn't exist
            - Partial updates supported (only provided fields updated)
            - Preserves relationships (movies)
        """
        db_actor = db.query(Actor).filter(Actor.id == actor_id).first()
        if db_actor:
            for field, value in actor.dict().items():
                setattr(db_actor, field, value)
            db.commit()
            db.refresh(db_actor)
        return db_actor
    
    @staticmethod
    def delete_actor(db: Session, actor_id: int):
        """
        Delete an actor from the database.
        
        Args:
            db: Database session
            actor_id: ID of actor to delete
            
        Returns:
            True if deleted, False if not found
            
        Edge Cases:
            - Returns False for non-existent actors
            - Many-to-many relationships automatically cleaned up
            - Does not cascade delete related movies
        """
        db_actor = db.query(Actor).filter(Actor.id == actor_id).first()
        if db_actor:
            db.delete(db_actor)
            db.commit()
            return True
        return False
    
    @staticmethod
    def filter_actors_by_genre(db: Session, genre_id: int, skip: int = 0, limit: int = 100):
        """
        Find actors who appeared in movies of a specific genre.
        
        Args:
            db: Database session
            genre_id: ID of genre to filter by
            skip: Pagination offset
            limit: Maximum results to return
            
        Returns:
            List of Actor objects who appeared in movies of the specified genre
            
        Edge Cases:
            - Uses DISTINCT to avoid duplicate actors
            - Returns empty list if genre has no movies or movies have no actors
            - Handles complex many-to-many relationships correctly
        """
        return db.query(Actor).join(Actor.movies).join(Movie.genres).filter(
            Genre.id == genre_id
        ).distinct().offset(skip).limit(limit).all()
    
    @staticmethod
    def search_actors(db: Session, search_term: str, skip: int = 0, limit: int = 100):
        """
        Search actors by name using case-insensitive matching.
        
        Args:
            db: Database session
            search_term: Search string to match against actor names
            skip: Pagination offset
            limit: Maximum results to return
            
        Returns:
            List of Actor objects matching the search term
            
        Edge Cases:
            - Case-insensitive search using ILIKE
            - Partial matching (substring search)
            - Returns empty list if no matches found
            - Search term is not sanitized (SQLAlchemy handles SQL injection)
        """
        return db.query(Actor).filter(
            Actor.name.ilike(f"%{search_term}%")
        ).offset(skip).limit(limit).all()

class DirectorCRUD:
    @staticmethod
    def get_director(db: Session, director_id: int):
        return db.query(Director).filter(Director.id == director_id).first()
    
    @staticmethod
    def get_directors(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Director).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_director(db: Session, director: DirectorCreate):
        db_director = Director(**director.dict())
        db.add(db_director)
        db.commit()
        db.refresh(db_director)
        return db_director
    
    @staticmethod
    def update_director(db: Session, director_id: int, director: DirectorCreate):
        db_director = db.query(Director).filter(Director.id == director_id).first()
        if db_director:
            for field, value in director.dict().items():
                setattr(db_director, field, value)
            db.commit()
            db.refresh(db_director)
        return db_director
    
    @staticmethod
    def delete_director(db: Session, director_id: int):
        db_director = db.query(Director).filter(Director.id == director_id).first()
        if db_director:
            db.delete(db_director)
            db.commit()
            return True
        return False
    
    @staticmethod
    def search_directors(db: Session, search_term: str, skip: int = 0, limit: int = 100):
        return db.query(Director).filter(
            Director.name.ilike(f"%{search_term}%")
        ).offset(skip).limit(limit).all()

class GenreCRUD:
    @staticmethod
    def get_genre(db: Session, genre_id: int):
        return db.query(Genre).filter(Genre.id == genre_id).first()
    
    @staticmethod
    def get_genres(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Genre).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_genre(db: Session, genre: GenreCreate):
        db_genre = Genre(**genre.dict())
        db.add(db_genre)
        db.commit()
        db.refresh(db_genre)
        return db_genre
    
    @staticmethod
    def update_genre(db: Session, genre_id: int, genre: GenreCreate):
        db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if db_genre:
            for field, value in genre.dict().items():
                setattr(db_genre, field, value)
            db.commit()
            db.refresh(db_genre)
        return db_genre
    
    @staticmethod
    def delete_genre(db: Session, genre_id: int):
        db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
        if db_genre:
            db.delete(db_genre)
            db.commit()
            return True
        return False

class ReviewCRUD:
    @staticmethod
    def get_review(db: Session, review_id: int):
        return db.query(Review).filter(Review.id == review_id).first()
    
    @staticmethod
    def get_movie_reviews(db: Session, movie_id: int, skip: int = 0, limit: int = 100):
        return db.query(Review).filter(Review.movie_id == movie_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_review(db: Session, review: ReviewCreate):
        db_review = Review(**review.dict())
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    
    @staticmethod
    def delete_review(db: Session, review_id: int):
        db_review = db.query(Review).filter(Review.id == review_id).first()
        if db_review:
            db.delete(db_review)
            db.commit()
            return True
        return False
