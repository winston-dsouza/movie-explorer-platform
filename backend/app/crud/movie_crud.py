from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.models.models import Movie, Actor, Director, Genre, Review
from app.schemas.schemas import MovieCreate, MovieUpdate

class MovieCRUD:
    @staticmethod
    def get_movie(db: Session, movie_id: int):
        return db.query(Movie).filter(Movie.id == movie_id).first()
    
    @staticmethod
    def get_movies(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Movie).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_movie(db: Session, movie: MovieCreate):
        # Create movie instance
        db_movie = Movie(
            title=movie.title,
            release_year=movie.release_year,
            description=movie.description,
            poster_url=movie.poster_url,
            rating=movie.rating,
            runtime_minutes=movie.runtime_minutes,
            director_id=movie.director_id
        )
        
        # Add genres
        if movie.genre_ids:
            genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()
            db_movie.genres = genres
        
        # Add actors
        if movie.actor_ids:
            actors = db.query(Actor).filter(Actor.id.in_(movie.actor_ids)).all()
            db_movie.actors = actors
        
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def update_movie(db: Session, movie_id: int, movie: MovieUpdate):
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not db_movie:
            return None
        
        # Update basic fields
        update_data = movie.dict(exclude_unset=True, exclude={'genre_ids', 'actor_ids'})
        for field, value in update_data.items():
            setattr(db_movie, field, value)
        
        # Update genres if provided
        if movie.genre_ids is not None:
            genres = db.query(Genre).filter(Genre.id.in_(movie.genre_ids)).all()
            db_movie.genres = genres
        
        # Update actors if provided
        if movie.actor_ids is not None:
            actors = db.query(Actor).filter(Actor.id.in_(movie.actor_ids)).all()
            db_movie.actors = actors
        
        db.commit()
        db.refresh(db_movie)
        return db_movie
    
    @staticmethod
    def delete_movie(db: Session, movie_id: int):
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if db_movie:
            db.delete(db_movie)
            db.commit()
            return True
        return False
    
    @staticmethod
    def filter_movies(
        db: Session,
        genre_id: Optional[int] = None,
        director_id: Optional[int] = None,
        release_year: Optional[int] = None,
        actor_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ):
        query = db.query(Movie)
        
        if genre_id:
            query = query.join(Movie.genres).filter(Genre.id == genre_id)
        
        if director_id:
            query = query.filter(Movie.director_id == director_id)
        
        if release_year:
            query = query.filter(Movie.release_year == release_year)
        
        if actor_id:
            query = query.join(Movie.actors).filter(Actor.id == actor_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def search_movies(db: Session, search_term: str, skip: int = 0, limit: int = 100):
        return db.query(Movie).filter(
            or_(
                Movie.title.ilike(f"%{search_term}%"),
                Movie.description.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit).all()
