from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.tutor import router as tutor_router
from backend.database.db import init_db
import config

app = FastAPI(
    title="CodeTutor - LLM-Powered Programming Tutor",
    description="An intelligent tutoring system for programming education based on open-source LLM",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tutor_router)


@app.on_event("startup")
async def startup():
    init_db()
    print("Database initialized.")
    print(f"Using LLM model: {config.LLM_MODEL}")


@app.get("/")
async def root():
    return {
        "name": "CodeTutor API",
        "version": "1.0.0",
        "status": "running",
        "model": config.LLM_MODEL,
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
