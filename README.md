<img width="1919" height="1019" alt="Screenshot 2026-05-08 140349" src="https://github.com/user-attachments/assets/1f78c14e-7afc-49ed-8862-3a466694a721" />
<img width="1919" height="1020" alt="Screenshot 2026-05-08 140411" src="https://github.com/user-attachments/assets/5817da5a-6684-4d9b-9891-095db613f838" />
<img width="1915" height="1020" alt="Screenshot 2026-05-08 140446" src="https://github.com/user-attachments/assets/ac3b51e8-9b4c-482a-8552-afe6aed33777" />
<img width="1919" height="1023" alt="Screenshot 2026-05-08 140523" src="https://github.com/user-attachments/assets/f186dae5-9950-4078-be36-4a779f631c7e" />
<img width="1919" height="1026" alt="Screenshot 2026-05-08 140546" src="https://github.com/user-attachments/assets/f6130722-82d2-4564-8212-8250e4e60668" />




# 🔗 URL Shortener API

A production-style REST API built with **FastAPI** that shortens long URLs, tracks click analytics, and supports custom aliases and link expiry.

## 🚀 Features

- **Shorten URLs** — Generate a unique short code for any URL
- **Custom Aliases** — Choose your own short code (e.g. `/github`)
- **Click Analytics** — Track how many times each link is clicked
- **Link Expiry** — Set URLs to auto-expire after N days
- **Auto Docs** — Interactive Swagger UI at `/docs`
- **Fully Tested** — Pytest test suite included

## 🛠️ Tech Stack

| Layer       | Tool                  |
|-------------|-----------------------|
| Framework   | FastAPI               |
| Database    | SQLite + SQLAlchemy   |
| Validation  | Pydantic v2           |
| Testing     | Pytest + HTTPX        |
| Server      | Uvicorn               |

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the API

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for the interactive Swagger UI.

## 🔌 API Endpoints

### `POST /shorten` — Shorten a URL

```json
// Request
{
  "original_url": "https://www.example.com/very/long/path",
  "alias": "mylink",       // optional
  "expiry_days": 7         // optional
}

// Response (201)
{
  "short_code": "mylink",
  "original_url": "https://www.example.com/very/long/path",
  "short_url": "http://localhost:8000/mylink",
  "created_at": "2024-01-01T10:00:00"
}
```

### `GET /{short_code}` — Redirect to original URL

Redirects with `302` status. Increments the click counter automatically.

### `GET /stats/{short_code}` — Get link statistics

```json
// Response (200)
{
  "short_code": "mylink",
  "original_url": "https://www.example.com/very/long/path",
  "click_count": 42,
  "created_at": "2024-01-01T10:00:00",
  "expires_at": "2024-01-08T10:00:00"
}
```

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 📁 Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app & route handlers
│   ├── models.py      # SQLAlchemy DB models
│   ├── schemas.py     # Pydantic request/response schemas
│   ├── crud.py        # Database operations
│   └── database.py    # DB connection & session
├── tests/
│   ├── __init__.py
│   └── test_api.py    # Pytest test suite
├── requirements.txt
└── README.md
```

## 🌐 Deployment

Deploy for free on [Render](https://render.com) or [Railway](https://railway.app):

1. Push your code to GitHub
2. Connect your repo to Render/Railway
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Update `BASE_URL` in `main.py` to your deployed URL
