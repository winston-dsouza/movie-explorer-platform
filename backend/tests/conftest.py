"""
Test configuration and fixtures for pytest.
Provides test database setup and FastAPI test client.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.models import Movie, Actor, Director, Genre, Review

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_genre(db_session):
    """Create a sample genre for testing."""
    genre = Genre(name="Action", description="Action movies")
    db_session.add(genre)
    db_session.commit()
    db_session.refresh(genre)
    return genre


@pytest.fixture
def sample_director(db_session):
    """Create a sample director for testing."""
    director = Director(
        name="Christopher Nolan",
        bio="British-American film director",
        birth_year=1970
    )
    db_session.add(director)
    db_session.commit()
    db_session.refresh(director)
    return director


@pytest.fixture
def sample_actor(db_session):
    """Create a sample actor for testing."""
    actor = Actor(
        name="Leonardo DiCaprio",
        bio="American actor and producer",
        birth_year=1974
    )
    db_session.add(actor)
    db_session.commit()
    db_session.refresh(actor)
    return actor


@pytest.fixture
def sample_movie(db_session, sample_genre, sample_director):
    """Create a sample movie for testing."""
    movie = Movie(
        title="Inception",
        description="A thief who steals corporate secrets",
        release_year=2010,
        duration=148,
        rating=8.8,
        poster_url="https://example.com/inception.jpg",
        director_id=sample_director.id
    )
    movie.genres.append(sample_genre)
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return movie
