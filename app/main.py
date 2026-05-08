from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine, get_db

# Create all database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A production-style REST API to shorten URLs, track clicks, and manage link expiry.",
    version="1.0.0",
)

BASE_URL = "http://localhost:8000"


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"message": "URL Shortener API is running!", "docs": f"{BASE_URL}/docs"}


@app.post("/shorten", response_model=schemas.URLResponse, status_code=201, tags=["URLs"])
def shorten_url(url_data: schemas.URLCreate, db: Session = Depends(get_db)):
    """
    Shorten a long URL.

    - **original_url**: The full URL to shorten (required)
    - **alias**: Optional custom short code (3-20 alphanumeric characters)
    - **expiry_days**: Optional number of days before the link expires
    """
    try:
        db_url = crud.create_short_url(db, url_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return schemas.URLResponse(
        short_code=db_url.short_code,
        original_url=db_url.original_url,
        short_url=f"{BASE_URL}/{db_url.short_code}",
        created_at=db_url.created_at,
    )


@app.get("/stats/{short_code}", response_model=schemas.URLStats, tags=["URLs"])
def get_stats(short_code: str, db: Session = Depends(get_db)):
    """
    Get statistics for a shortened URL.

    Returns the original URL, total click count, creation date, and expiry date.
    """
    db_url = crud.get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return db_url


@app.get("/{short_code}", tags=["Redirect"])
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redirect to the original URL using the short code.

    Also increments the click counter for analytics.
    """
    db_url = crud.get_url_by_code(db, short_code)

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if crud.is_expired(db_url):
        raise HTTPException(status_code=410, detail="This link has expired")

    crud.increment_click_count(db, db_url)
    return RedirectResponse(url=db_url.original_url, status_code=302)
