import sys
import os

# Fix import path for Render/Gunicorn
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analyzer import InstagramAnalyzer

app = FastAPI()

# Allow CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = InstagramAnalyzer()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Instagram Analyzer Backend Running"}

@app.get("/analyze/{username}")
def analyze(username: str):
    data = analyzer.analyze_profile(username)
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
