import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create tables before tests
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "URL Shortener API is running" in response.json()["message"]


def test_shorten_url():
    response = client.post("/shorten", json={"original_url": "https://www.google.com"})
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["original_url"] == "https://www.google.com/"


def test_shorten_url_with_alias():
    response = client.post(
        "/shorten",
        json={"original_url": "https://www.github.com", "alias": "github"},
    )
    assert response.status_code == 201
    assert response.json()["short_code"] == "github"


def test_shorten_url_duplicate_alias():
    client.post("/shorten", json={"original_url": "https://example.com", "alias": "mylink"})
    response = client.post(
        "/shorten",
        json={"original_url": "https://another.com", "alias": "mylink"},
    )
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"]


def test_redirect():
    # First shorten a URL
    shorten_response = client.post(
        "/shorten",
        json={"original_url": "https://www.python.org", "alias": "python"},
    )
    short_code = shorten_response.json()["short_code"]

    # Now test redirect (allow_redirects=False to catch the 302)
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.python.org/"


def test_stats():
    client.post("/shorten", json={"original_url": "https://www.fastapi.tiangolo.com", "alias": "fastapi"})
    client.get("/fastapi", follow_redirects=False)
    client.get("/fastapi", follow_redirects=False)

    response = client.get("/stats/fastapi")
    assert response.status_code == 200
    data = response.json()
    assert data["click_count"] == 2
    assert data["short_code"] == "fastapi"


def test_not_found():
    response = client.get("/nonexistentcode")
    assert response.status_code == 404


def test_invalid_url():
    response = client.post("/shorten", json={"original_url": "not-a-valid-url"})
    assert response.status_code == 422
