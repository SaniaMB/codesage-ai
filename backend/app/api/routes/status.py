from fastapi import APIRouter
from app.engines.ai_engine import context_store

router = APIRouter()


@router.get("/status")
def status():

    print("Repository URL:", context_store.current_repository_url)
    print("Chunks:", len(context_store.repository_chunks))

    return {
        "repository_loaded": (
                context_store.current_repository_url is not None
                and len(context_store.repository_chunks) > 0
        ),
        "repository_url": context_store.current_repository_url
    }