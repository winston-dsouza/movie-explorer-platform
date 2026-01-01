from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.crud import GenreCRUD
from app.schemas.schemas import Genre, GenreCreate

router = APIRouter()

@router.get("/", response_model=List[Genre], summary="Get all genres", tags=["Genres"])
def get_genres(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all genres with pagination.
    """
    return GenreCRUD.get_genres(db, skip=skip, limit=limit)

@router.get("/{genre_id}", response_model=Genre, summary="Get genre by ID", tags=["Genres"])
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific genre.
    """
    genre = GenreCRUD.get_genre(db, genre_id=genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@router.post("/", response_model=Genre, summary="Create a new genre", tags=["Genres"])
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    """
    Create a new genre.
    """
    return GenreCRUD.create_genre(db, genre=genre)

@router.put("/{genre_id}", response_model=Genre, summary="Update a genre", tags=["Genres"])
def update_genre(genre_id: int, genre: GenreCreate, db: Session = Depends(get_db)):
    """
    Update an existing genre.
    """
    db_genre = GenreCRUD.update_genre(db, genre_id=genre_id, genre=genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@router.delete("/{genre_id}", summary="Delete a genre", tags=["Genres"])
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Delete a genre.
    """
    if not GenreCRUD.delete_genre(db, genre_id=genre_id):
        raise HTTPException(status_code=404, detail="Genre not found")
    return {"message": "Genre deleted successfully"}
