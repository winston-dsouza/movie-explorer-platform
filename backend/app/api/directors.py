from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.crud import DirectorCRUD
from app.schemas.schemas import Director, DirectorCreate, DirectorWithMovies

router = APIRouter()

@router.get("/", response_model=List[Director], summary="Get all directors", tags=["Directors"])
def get_directors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all directors with pagination.
    """
    return DirectorCRUD.get_directors(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[Director], summary="Search directors", tags=["Directors"])
def search_directors(
    q: str = Query(..., description="Search term for director name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Search directors by name.
    """
    return DirectorCRUD.search_directors(db, search_term=q, skip=skip, limit=limit)

@router.get("/{director_id}", response_model=DirectorWithMovies, summary="Get director by ID", tags=["Directors"])
def get_director(director_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific director including their movies.
    """
    director = DirectorCRUD.get_director(db, director_id=director_id)
    if director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@router.post("/", response_model=Director, summary="Create a new director", tags=["Directors"])
def create_director(director: DirectorCreate, db: Session = Depends(get_db)):
    """
    Create a new director.
    """
    return DirectorCRUD.create_director(db, director=director)

@router.put("/{director_id}", response_model=Director, summary="Update a director", tags=["Directors"])
def update_director(director_id: int, director: DirectorCreate, db: Session = Depends(get_db)):
    """
    Update an existing director.
    """
    db_director = DirectorCRUD.update_director(db, director_id=director_id, director=director)
    if db_director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return db_director

@router.delete("/{director_id}", summary="Delete a director", tags=["Directors"])
def delete_director(director_id: int, db: Session = Depends(get_db)):
    """
    Delete a director.
    """
    if not DirectorCRUD.delete_director(db, director_id=director_id):
        raise HTTPException(status_code=404, detail="Director not found")
    return {"message": "Director deleted successfully"}
