from fastapi import APIRouter

from app.schemas.scan import ScanRequest

from app.engines.project_engine.scanner import ProjectScanner
from app.engines.analysis_engine.analyzer import ProjectAnalyzer
from app.engines.analysis_engine.parser import PythonParser

from app.engines.ai_engine import context_store
from app.engines.ai_engine import chat_memory
from app.engines.ai_engine.context_builder import ProjectContextBuilder
from app.engines.ai_engine.chunk_builder import ChunkBuilder
from app.engines.ai_engine.embedding_client import EmbeddingClient

router = APIRouter()

scanner = ProjectScanner()
analyzer = ProjectAnalyzer()
parser = PythonParser()
context_builder = ProjectContextBuilder()
chunk_builder = ChunkBuilder()
embedding_client = EmbeddingClient()


@router.post("/scan")
def scan_repository(request: ScanRequest):

    # Repository already indexed
    if context_store.current_repository_url == request.repository:
        return {
            "message": "Repository already analyzed.",
            "already_scanned": True
        }

    # Clone repository
    repository_path = scanner.clone_repository(request.repository)

    # Find Python files
    python_files = analyzer.get_python_files(repository_path)

    analysis = []

    # Analyze every Python file
    for file in python_files:

        file_analysis = parser.parse_file(file)

        analysis.append({
            "file": str(file),
            **file_analysis
        })

    # Build chunks
    chunks = chunk_builder.build_chunks(analysis)

    print(f"Total chunks created: {len(chunks)}")

    repository_chunks = []

    # Generate embeddings
    for chunk in chunks:

        embedding = embedding_client.embed(chunk["content"])

        repository_chunks.append({
            "chunk": chunk,
            "embedding": embedding
        })

    # Store repository in memory
    context_store.repository_chunks = repository_chunks
    context_store.current_repository_url = request.repository

    # New repository -> clear previous conversation
    chat_memory.conversation_history = []

    return {
        "message": "Repository analyzed successfully!",
        "chunks_indexed": len(chunks)
    }