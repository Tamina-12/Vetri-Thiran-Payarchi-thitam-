from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.routes import router


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-assisted legal document generation API"
    ),
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



@app.get("/")
async def root():

    
        return {
    "message": "Welcome to LegalEase AI Legal Document Generator API",
    "status": "running"
}


app.include_router(router)