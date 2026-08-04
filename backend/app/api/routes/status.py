from fastapi import APIRouter
from app.engines.ai_engine import context_store

router = APIRouter()


@router.get("/status")
def status():

    return {
        "repository_loaded": context_store.current_repository_url is not None,
        "repository_url": context_store.current_repository_url
    }