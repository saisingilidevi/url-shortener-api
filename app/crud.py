import random
import string
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app import models, schemas


def generate_short_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))


def get_url_by_code(db: Session, short_code: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()


def get_url_by_original(db: Session, original_url: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.original_url == original_url).first()


def create_short_url(db: Session, url_data: schemas.URLCreate) -> models.URL:
    original_url = str(url_data.original_url)

    # Use custom alias or generate a unique code
    if url_data.alias:
        short_code = url_data.alias
        if get_url_by_code(db, short_code):
            raise ValueError(f"Alias '{short_code}' is already taken.")
    else:
        # Generate a unique short code
        for _ in range(10):
            short_code = generate_short_code()
            if not get_url_by_code(db, short_code):
                break
        else:
            raise RuntimeError("Could not generate a unique short code. Try again.")

    # Calculate expiry if provided
    expires_at = None
    if url_data.expiry_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=url_data.expiry_days)

    db_url = models.URL(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def increment_click_count(db: Session, db_url: models.URL) -> models.URL:
    db_url.click_count += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def is_expired(db_url: models.URL) -> bool:
    if db_url.expires_at is None:
        return False
    return datetime.now(timezone.utc) > db_url.expires_at.replace(tzinfo=timezone.utc)
