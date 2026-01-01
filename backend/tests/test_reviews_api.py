"""
Unit tests for review API endpoints.
Tests CRUD operations and validation.
"""

import pytest
from fastapi import status


class TestReviewsAPI:
    """Test suite for /api/reviews endpoints."""

    def test_create_review_success(self, client, sample_movie):
        """Test POST /api/reviews creates a new review successfully."""
        review_data = {
            "movie_id": sample_movie.id,
            "author": "John Doe",
            "rating": 9,
            "comment": "Amazing movie! Highly recommended."
        }
        response = client.post("/api/reviews", json=review_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["author"] == "John Doe"
        assert data["rating"] == 9
        assert "id" in data

    def test_create_review_invalid_movie(self, client):
        """Test POST /api/reviews with non-existent movie returns 404."""
        review_data = {
            "movie_id": 99999,
            "author": "John Doe",
            "rating": 9,
            "comment": "Test review"
        }
        response = client.post("/api/reviews", json=review_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_review_invalid_rating(self, client, sample_movie):
        """Test POST /api/reviews with invalid rating (out of 1-10 range)."""
        review_data = {
            "movie_id": sample_movie.id,
            "author": "John Doe",
            "rating": 15,  # Invalid: > 10
            "comment": "Test"
        }
        response = client.post("/api/reviews", json=review_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_reviews_for_movie(self, client, db_session, sample_movie):
        """Test GET /api/reviews/movie/{movie_id} returns all reviews for a movie."""
        # Create multiple reviews
        from app.models.models import Review
        
        review1 = Review(movie_id=sample_movie.id, author="User1", rating=8, comment="Good")
        review2 = Review(movie_id=sample_movie.id, author="User2", rating=9, comment="Great")
        db_session.add_all([review1, review2])
        db_session.commit()
        
        response = client.get(f"/api/reviews/movie/{sample_movie.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_get_reviews_for_nonexistent_movie(self, client):
        """Test GET /api/reviews/movie/{movie_id} returns empty list for movie with no reviews."""
        response = client.get("/api/reviews/movie/99999")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_delete_review(self, client, db_session, sample_movie):
        """Test DELETE /api/reviews/{id} removes review successfully."""
        from app.models.models import Review
        
        review = Review(movie_id=sample_movie.id, author="User", rating=8, comment="Test")
        db_session.add(review)
        db_session.commit()
        db_session.refresh(review)
        
        response = client.delete(f"/api/reviews/{review.id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify review is deleted
        reviews_response = client.get(f"/api/reviews/movie/{sample_movie.id}")
        assert len(reviews_response.json()) == 0

    def test_delete_nonexistent_review(self, client):
        """Test DELETE /api/reviews/{id} returns 404 for non-existent review."""
        response = client.delete("/api/reviews/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
