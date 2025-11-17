import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Photo, Song, Movie, Note, Plan

app = FastAPI(title="Couples App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Couples App Backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Re-check envs explicitly
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# -----------------------------
# Helper
# -----------------------------
class IdModel(BaseModel):
    id: str


def to_serializable(doc):
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


# -----------------------------
# Photos (with favorites support)
# -----------------------------
@app.post("/photos", response_model=dict)
async def add_photo(photo: Photo):
    inserted_id = create_document("photo", photo)
    return {"id": inserted_id}

@app.get("/photos", response_model=List[dict])
async def list_photos(favorites: Optional[bool] = None):
    filter_q = {}
    if favorites is not None:
        filter_q["favorite"] = favorites
    docs = get_documents("photo", filter_q)
    return [to_serializable(d) for d in docs]

# -----------------------------
# Songs
# -----------------------------
@app.post("/songs", response_model=dict)
async def add_song(song: Song):
    inserted_id = create_document("song", song)
    return {"id": inserted_id}

@app.get("/songs", response_model=List[dict])
async def list_songs():
    docs = get_documents("song")
    return [to_serializable(d) for d in docs]

# -----------------------------
# Movies
# -----------------------------
@app.post("/movies", response_model=dict)
async def add_movie(movie: Movie):
    inserted_id = create_document("movie", movie)
    return {"id": inserted_id}

@app.get("/movies", response_model=List[dict])
async def list_movies():
    docs = get_documents("movie")
    return [to_serializable(d) for d in docs]

# -----------------------------
# Notes
# -----------------------------
@app.post("/notes", response_model=dict)
async def add_note(note: Note):
    inserted_id = create_document("note", note)
    return {"id": inserted_id}

@app.get("/notes", response_model=List[dict])
async def list_notes():
    docs = get_documents("note")
    return [to_serializable(d) for d in docs]

# -----------------------------
# Plans
# -----------------------------
@app.post("/plans", response_model=dict)
async def add_plan(plan: Plan):
    inserted_id = create_document("plan", plan)
    return {"id": inserted_id}

@app.get("/plans", response_model=List[dict])
async def list_plans():
    docs = get_documents("plan")
    return [to_serializable(d) for d in docs]


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
