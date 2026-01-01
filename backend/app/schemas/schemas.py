from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

# Genre Schemas
class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Director Schemas
class DirectorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    photo_url: Optional[str] = None
    nationality: Optional[str] = None

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DirectorWithMovies(Director):
    movies: List['MovieSimple'] = []

# Actor Schemas
class ActorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    photo_url: Optional[str] = None
    nationality: Optional[str] = None

class ActorCreate(ActorBase):
    pass

class Actor(ActorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ActorWithMovies(Actor):
    movies: List['MovieSimple'] = []

# Review Schemas
class ReviewBase(BaseModel):
    reviewer_name: str
    rating: float
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    movie_id: int

class Review(ReviewBase):
    id: int
    movie_id: int
    created_at: Optional[date] = None
    model_config = ConfigDict(from_attributes=True)

# Movie Schemas
class MovieBase(BaseModel):
    title: str
    release_year: int
    description: Optional[str] = None
    poster_url: Optional[str] = None
    rating: Optional[float] = 0.0
    runtime_minutes: Optional[int] = None

class MovieCreate(MovieBase):
    director_id: Optional[int] = None
    genre_ids: List[int] = []
    actor_ids: List[int] = []

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    rating: Optional[float] = None
    runtime_minutes: Optional[int] = None
    director_id: Optional[int] = None
    genre_ids: Optional[List[int]] = None
    actor_ids: Optional[List[int]] = None

class MovieSimple(MovieBase):
    id: int
    director: Optional[Director] = None
    genres: List[Genre] = []
    model_config = ConfigDict(from_attributes=True)

class Movie(MovieBase):
    id: int
    director: Optional[Director] = None
    genres: List[Genre] = []
    actors: List[Actor] = []
    reviews: List[Review] = []
    model_config = ConfigDict(from_attributes=True)

# Update forward references
DirectorWithMovies.model_rebuild()
ActorWithMovies.model_rebuild()
