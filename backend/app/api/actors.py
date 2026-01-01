from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.crud.crud import ActorCRUD
from app.schemas.schemas import Actor, ActorCreate, ActorWithMovies

router = APIRouter()

@router.get("/", response_model=List[Actor], summary="Get all actors", tags=["Actors"])
def get_actors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all actors with pagination.
    """
    return ActorCRUD.get_actors(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[Actor], summary="Search actors", tags=["Actors"])
def search_actors(
    q: str = Query(..., description="Search term for actor name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Search actors by name.
    """
    return ActorCRUD.search_actors(db, search_term=q, skip=skip, limit=limit)

@router.get("/by-genre/{genre_id}", response_model=List[Actor], summary="Get actors by genre", tags=["Actors"])
def get_actors_by_genre(
    genre_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get actors who have acted in movies of a specific genre.
    """
    return ActorCRUD.filter_actors_by_genre(db, genre_id=genre_id, skip=skip, limit=limit)

@router.get("/{actor_id}", response_model=ActorWithMovies, summary="Get actor by ID", tags=["Actors"])
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific actor including their movies.
    """
    actor = ActorCRUD.get_actor(db, actor_id=actor_id)
    if actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

@router.post("/", response_model=Actor, summary="Create a new actor", tags=["Actors"])
def create_actor(actor: ActorCreate, db: Session = Depends(get_db)):
    """
    Create a new actor.
    """
    return ActorCRUD.create_actor(db, actor=actor)

@router.put("/{actor_id}", response_model=Actor, summary="Update an actor", tags=["Actors"])
def update_actor(actor_id: int, actor: ActorCreate, db: Session = Depends(get_db)):
    """
    Update an existing actor.
    """
    db_actor = ActorCRUD.update_actor(db, actor_id=actor_id, actor=actor)
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Actor not found")
    return db_actor

@router.delete("/{actor_id}", summary="Delete an actor", tags=["Actors"])
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    """
    Delete an actor.
    """
    if not ActorCRUD.delete_actor(db, actor_id=actor_id):
        raise HTTPException(status_code=404, detail="Actor not found")
    return {"message": "Actor deleted successfully"}
