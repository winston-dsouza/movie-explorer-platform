from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.crud.crud import ReviewCRUD
from app.schemas.schemas import Review, ReviewCreate

router = APIRouter()

@router.get("/movie/{movie_id}", response_model=List[Review], summary="Get reviews for a movie", tags=["Reviews"])
def get_movie_reviews(
    movie_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a specific movie.
    """
    return ReviewCRUD.get_movie_reviews(db, movie_id=movie_id, skip=skip, limit=limit)

@router.get("/{review_id}", response_model=Review, summary="Get review by ID", tags=["Reviews"])
def get_review(review_id: int, db: Session = Depends(get_db)):
    """
    Get a specific review by ID.
    """
    review = ReviewCRUD.get_review(db, review_id=review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.post("/", response_model=Review, summary="Create a new review", tags=["Reviews"])
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Create a new review for a movie.
    """
    return ReviewCRUD.create_review(db, review=review)

@router.delete("/{review_id}", summary="Delete a review", tags=["Reviews"])
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """
    Delete a review.
    """
    if not ReviewCRUD.delete_review(db, review_id=review_id):
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
