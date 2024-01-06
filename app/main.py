from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.v1 import router as v1_router

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, version="0.0.1")

    ORIGINS = ["http://localhost:8000","http://127.0.0.1:8080", "https://localhost:8000", "http://localhost:3000", "http://localhost", "https://localhost"]
    _app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(v1_router, prefix="/api")

@app.get("/")
def root():
    return {"Message": "Hello There"}
