"""
Unit tests for movie API endpoints.
Tests CRUD operations, filtering, search, and edge cases.
"""

import pytest
from fastapi import status


class TestMoviesAPI:
    """Test suite for /api/movies endpoints."""

    def test_get_movies_empty_database(self, client):
        """Test GET /api/movies returns empty list when no movies exist."""
        response = client.get("/api/movies")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_movie_success(self, client, sample_director, sample_genre):
        """Test POST /api/movies creates a new movie successfully."""
        movie_data = {
            "title": "The Matrix",
            "description": "A computer hacker learns about the true nature of reality",
            "release_year": 1999,
            "duration": 136,
            "rating": 8.7,
            "poster_url": "https://example.com/matrix.jpg",
            "director_id": sample_director.id,
            "genre_ids": [sample_genre.id]
        }
        response = client.post("/api/movies", json=movie_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "The Matrix"
        assert data["release_year"] == 1999
        assert "id" in data

    def test_create_movie_invalid_director(self, client, sample_genre):
        """Test POST /api/movies with non-existent director returns 404."""
        movie_data = {
            "title": "Test Movie",
            "description": "Test description",
            "release_year": 2020,
            "duration": 120,
            "rating": 7.5,
            "director_id": 99999,  # Non-existent director
            "genre_ids": [sample_genre.id]
        }
        response = client.post("/api/movies", json=movie_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_movie_by_id(self, client, sample_movie):
        """Test GET /api/movies/{id} returns correct movie details."""
        response = client.get(f"/api/movies/{sample_movie.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_movie.id
        assert data["title"] == sample_movie.title
        assert "director" in data
        assert "genres" in data
        assert "actors" in data

    def test_get_movie_not_found(self, client):
        """Test GET /api/movies/{id} returns 404 for non-existent movie."""
        response = client.get("/api/movies/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_movie(self, client, sample_movie):
        """Test PUT /api/movies/{id} updates movie successfully."""
        update_data = {
            "title": "Inception Updated",
            "description": "Updated description",
            "release_year": 2010,
            "duration": 150,
            "rating": 9.0,
            "director_id": sample_movie.director_id,
            "genre_ids": [g.id for g in sample_movie.genres]
        }
        response = client.put(f"/api/movies/{sample_movie.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Inception Updated"
        assert data["rating"] == 9.0

    def test_delete_movie(self, client, sample_movie):
        """Test DELETE /api/movies/{id} removes movie successfully."""
        movie_id = sample_movie.id
        response = client.delete(f"/api/movies/{movie_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify movie is deleted
        get_response = client.get(f"/api/movies/{movie_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_search_movies_by_title(self, client, sample_movie):
        """Test GET /api/movies/search finds movies by title."""
        response = client.get("/api/movies/search?query=Inception")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert any(movie["title"] == "Inception" for movie in data)

    def test_search_movies_case_insensitive(self, client, sample_movie):
        """Test search is case-insensitive."""
        response = client.get("/api/movies/search?query=inception")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0

    def test_search_movies_no_results(self, client):
        """Test search returns empty list when no matches found."""
        response = client.get("/api/movies/search?query=NonexistentMovie12345")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_filter_movies_by_genre(self, client, sample_movie, sample_genre):
        """Test GET /api/movies filters by genre_id."""
        response = client.get(f"/api/movies?genre_id={sample_genre.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert all(any(g["id"] == sample_genre.id for g in movie["genres"]) for movie in data)

    def test_filter_movies_by_director(self, client, sample_movie, sample_director):
        """Test GET /api/movies filters by director_id."""
        response = client.get(f"/api/movies?director_id={sample_director.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert all(movie["director"]["id"] == sample_director.id for movie in data)

    def test_filter_movies_by_actor(self, client, db_session, sample_movie, sample_actor):
        """Test GET /api/movies filters by actor_id."""
        # Add actor to movie
        sample_movie.actors.append(sample_actor)
        db_session.commit()
        
        response = client.get(f"/api/movies?actor_id={sample_actor.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert all(any(a["id"] == sample_actor.id for a in movie["actors"]) for movie in data)

    def test_create_movie_with_invalid_rating(self, client, sample_director, sample_genre):
        """Test POST /api/movies with invalid rating (out of 0-10 range)."""
        movie_data = {
            "title": "Test Movie",
            "description": "Test",
            "release_year": 2020,
            "duration": 120,
            "rating": 15.0,  # Invalid: > 10
            "director_id": sample_director.id,
            "genre_ids": [sample_genre.id]
        }
        response = client.post("/api/movies", json=movie_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_movie_missing_required_fields(self, client):
        """Test POST /api/movies fails with missing required fields."""
        movie_data = {
            "title": "Incomplete Movie"
            # Missing required fields
        }
        response = client.post("/api/movies", json=movie_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
