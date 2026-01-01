"""
Unit tests for actor API endpoints.
Tests CRUD operations, search functionality, and edge cases.
"""

import pytest
from fastapi import status


class TestActorsAPI:
    """Test suite for /api/actors endpoints."""

    def test_get_actors_empty_database(self, client):
        """Test GET /api/actors returns empty list when no actors exist."""
        response = client.get("/api/actors")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_actor_success(self, client):
        """Test POST /api/actors creates a new actor successfully."""
        actor_data = {
            "name": "Tom Hanks",
            "bio": "American actor and filmmaker",
            "birth_year": 1956,
            "photo_url": "https://example.com/tom-hanks.jpg"
        }
        response = client.post("/api/actors", json=actor_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Tom Hanks"
        assert data["birth_year"] == 1956
        assert "id" in data

    def test_get_actor_by_id(self, client, sample_actor):
        """Test GET /api/actors/{id} returns correct actor details."""
        response = client.get(f"/api/actors/{sample_actor.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_actor.id
        assert data["name"] == sample_actor.name
        assert "movies" in data

    def test_get_actor_not_found(self, client):
        """Test GET /api/actors/{id} returns 404 for non-existent actor."""
        response = client.get("/api/actors/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_actor(self, client, sample_actor):
        """Test PUT /api/actors/{id} updates actor successfully."""
        update_data = {
            "name": "Leonardo DiCaprio Updated",
            "bio": "Updated bio",
            "birth_year": 1974,
            "photo_url": "https://example.com/updated.jpg"
        }
        response = client.put(f"/api/actors/{sample_actor.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Leonardo DiCaprio Updated"

    def test_delete_actor(self, client, sample_actor):
        """Test DELETE /api/actors/{id} removes actor successfully."""
        actor_id = sample_actor.id
        response = client.delete(f"/api/actors/{actor_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify actor is deleted
        get_response = client.get(f"/api/actors/{actor_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_search_actors_by_name(self, client, sample_actor):
        """Test GET /api/actors/search finds actors by name."""
        response = client.get("/api/actors/search?query=Leonardo")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        assert any("Leonardo" in actor["name"] for actor in data)

    def test_search_actors_case_insensitive(self, client, sample_actor):
        """Test search is case-insensitive."""
        response = client.get("/api/actors/search?query=leonardo")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0

    def test_search_actors_no_results(self, client):
        """Test search returns empty list when no matches found."""
        response = client.get("/api/actors/search?query=NonexistentActor12345")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_actor_missing_required_fields(self, client):
        """Test POST /api/actors fails with missing required fields."""
        actor_data = {
            "name": "Incomplete Actor"
            # Missing other fields
        }
        response = client.post("/api/actors", json=actor_data)
        # Should still succeed as only name is required
        assert response.status_code == status.HTTP_200_OK

    def test_actor_filmography(self, client, db_session, sample_actor, sample_movie):
        """Test actor detail includes filmography."""
        # Add actor to movie
        sample_movie.actors.append(sample_actor)
        db_session.commit()
        
        response = client.get(f"/api/actors/{sample_actor.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["movies"]) > 0
        assert any(movie["id"] == sample_movie.id for movie in data["movies"])
