from fastapi import APIRouter
from app.engines.ai_engine.ollama_client import OllamaClient
from app.schemas.ask import AskRequest
from app.engines.ai_engine import context_store
from app.engines.ai_engine.retriever import Retriever
from app.engines.ai_engine import chat_memory

router = APIRouter()

ollamaClient = OllamaClient()
retriever = Retriever()


@router.post("/ask")
def ask(request: AskRequest):

    if not context_store.repository_chunks:
        return {
            "error": "No repository has been scanned yet."
        }

    # Retrieve the most relevant chunks
    retrieved_chunks = retriever.retrieve(
        context_store.repository_chunks,
        request.question
    )

    # Expand each retrieved chunk into all parts of the same class/function
    expanded_chunks = []
    seen = set()

    for retrieved in retrieved_chunks:

        key = (
            retrieved["file"],
            retrieved["name"]
        )

        if key in seen:
            continue

        seen.add(key)

        for item in context_store.repository_chunks:

            chunk = item["chunk"]

            if (
                chunk["file"] == retrieved["file"]
                and chunk["name"] == retrieved["name"]
            ):
                expanded_chunks.append(chunk)

    # Build repository context
    context = ""

    for chunk in expanded_chunks:

        context += (
            f"Type: {chunk['type']}\n"
            f"File: {chunk['file']}\n"
            f"Name: {chunk['name']}\n\n"
            f"{chunk['content']}\n\n"
            f"{'=' * 80}\n\n"
        )

    history = "\n".join(chat_memory.conversation_history)

    print("=" * 80)
    print("CONTEXT SENT TO MODEL:")
    print(context)
    print("=" * 80)

    answer = ollamaClient.generate(
        context,
        history,
        request.question
    )

    chat_memory.conversation_history.append(
        f"User: {request.question}"
    )

    chat_memory.conversation_history.append(
        f"Assistant: {answer}"
    )

    # Keep only the latest 5 conversations (10 entries)
    chat_memory.conversation_history = (
        chat_memory.conversation_history[-10:]
    )

    return {
        "answer": answer
    }