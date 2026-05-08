from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl
    alias: Optional[str] = None
    expiry_days: Optional[int] = None

    @field_validator("alias")
    @classmethod
    def alias_alphanumeric(cls, v):
        if v is not None:
            if not v.isalnum() or len(v) < 3 or len(v) > 20:
                raise ValueError("Alias must be 3-20 alphanumeric characters")
        return v


class URLResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime

    class Config:
        from_attributes = True


class URLStats(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True
