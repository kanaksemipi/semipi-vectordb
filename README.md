# 🧠 Flask + ChromaDB Vector Store API

A Flask-based API service for storing and querying property-related documents using vector embeddings with ChromaDB.

## 🚀 Features

- Add, update, delete, and view property documents
- Embed documents using SentenceTransformer (`BAAI/bge-large-en`)
- Query similar documents using vector search
- Pydantic-based data validation
- API key-based authentication
- Persistent ChromaDB storage

## 🗂️ Folder Structure

```
flask_chroma/
├── app/
│   ├── routes/
│   │   └── api_routes.py     # Main API endpoints
│   ├── __init__.py           # Flask app factory
│   ├── auth.py               # Auth decorator using API key
│   └── chroma_client.py      # ChromaDB client initialization
├── chroma_db/                # Chroma DB storage (can be ignored)
├── .env                      # Contains the API_KEY
├── config.py                 # App config loader using dotenv
├── run.py                    # Main entry point
├── test_api.py               # Test script for the endpoints
├── requirements.txt          # Required packages
└── .gitignore                # Git ignore rules
```

## 🔐 Authentication

All endpoints require an `x-api-key` header to be present in requests.

You can find your key in the `.env` file:
```
API_KEY=your-very-strong-secret-key
```

## 📦 Setup Instructions

1. **Clone this repository**
```bash
git clone https://github.com/your-username/flask-chroma.git
cd flask-chroma
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Flask server**
```bash
python run.py
```

5. **Test the API**
```bash
python test_api.py
```

## 🧪 Testing

- All endpoints are tested via `test_api.py`
- Make sure your server is running before executing tests

## 🛡️ Note

Do **not** expose the `.env` file in production. This is included only for demo/testing convenience.

---

Made with ❤️ by Abishek Chakravarthy
