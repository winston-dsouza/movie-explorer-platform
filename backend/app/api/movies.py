from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.crud.movie_crud import MovieCRUD
from app.schemas.schemas import Movie, MovieCreate, MovieUpdate, MovieSimple

router = APIRouter()

@router.get("/", response_model=List[MovieSimple], summary="Get all movies", tags=["Movies"])
def get_movies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all movies with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    """
    return MovieCRUD.get_movies(db, skip=skip, limit=limit)

@router.get("/filter", response_model=List[MovieSimple], summary="Filter movies", tags=["Movies"])
def filter_movies(
    genre_id: Optional[int] = Query(None, description="Filter by genre ID"),
    director_id: Optional[int] = Query(None, description="Filter by director ID"),
    release_year: Optional[int] = Query(None, description="Filter by release year"),
    actor_id: Optional[int] = Query(None, description="Filter by actor ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Filter movies by various criteria.
    
    - **genre_id**: Filter by genre ID
    - **director_id**: Filter by director ID
    - **release_year**: Filter by release year
    - **actor_id**: Filter by actor ID
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    return MovieCRUD.filter_movies(
        db, 
        genre_id=genre_id,
        director_id=director_id,
        release_year=release_year,
        actor_id=actor_id,
        skip=skip,
        limit=limit
    )

@router.get("/search", response_model=List[MovieSimple], summary="Search movies", tags=["Movies"])
def search_movies(
    q: str = Query(..., description="Search term for movie title or description"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Search movies by title or description.
    
    - **q**: Search term to match against movie title or description
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    return MovieCRUD.search_movies(db, search_term=q, skip=skip, limit=limit)

@router.get("/{movie_id}", response_model=Movie, summary="Get movie by ID", tags=["Movies"])
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific movie.
    
    - **movie_id**: The ID of the movie to retrieve
    """
    movie = MovieCRUD.get_movie(db, movie_id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=Movie, summary="Create a new movie", tags=["Movies"])
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie.
    
    - **title**: Movie title (required)
    - **release_year**: Year of release (required)
    - **description**: Movie description
    - **poster_url**: URL to movie poster image
    - **rating**: Movie rating (0-10)
    - **runtime_minutes**: Movie runtime in minutes
    - **director_id**: ID of the movie director
    - **genre_ids**: List of genre IDs
    - **actor_ids**: List of actor IDs
    """
    return MovieCRUD.create_movie(db, movie=movie)

@router.put("/{movie_id}", response_model=Movie, summary="Update a movie", tags=["Movies"])
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    """
    Update an existing movie.
    
    - **movie_id**: The ID of the movie to update
    """
    db_movie = MovieCRUD.update_movie(db, movie_id=movie_id, movie=movie)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.delete("/{movie_id}", summary="Delete a movie", tags=["Movies"])
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie.
    
    - **movie_id**: The ID of the movie to delete
    """
    if not MovieCRUD.delete_movie(db, movie_id=movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}
