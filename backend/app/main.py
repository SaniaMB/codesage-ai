from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.scan import router as scan_router
from app.api.routes.ask import router as ask_router
from app.api.routes.status import router as status_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to CodeSage AI 🚀"}

app.include_router(scan_router)
app.include_router(ask_router)

app.include_router(status_router)