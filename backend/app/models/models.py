from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association tables for many-to-many relationships
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

movie_actors = Table(
    'movie_actors',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    release_year = Column(Integer, nullable=False)
    description = Column(Text)
    poster_url = Column(String)
    rating = Column(Float, default=0.0)
    runtime_minutes = Column(Integer)
    
    # Foreign key for director
    director_id = Column(Integer, ForeignKey('directors.id'))
    
    # Relationships
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actors, back_populates="movies")
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")

class Actor(Base):
    __tablename__ = "actors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    bio = Column(Text)
    birth_date = Column(Date)
    photo_url = Column(String)
    nationality = Column(String)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_actors, back_populates="actors")

class Director(Base):
    __tablename__ = "directors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    bio = Column(Text)
    birth_date = Column(Date)
    photo_url = Column(String)
    nationality = Column(String)
    
    # Relationships
    movies = relationship("Movie", back_populates="director")

class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    reviewer_name = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(Text)
    created_at = Column(Date)
    
    # Relationships
    movie = relationship("Movie", back_populates="reviews")
