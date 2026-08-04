<div align="center">

# CodeSage AI

*Paste a repo. Ask it questions. Skip the part where you dig through 200 files to find the one that matters.*

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-1a1a1a?style=flat-square&logo=ollama&logoColor=white)
![React](https://img.shields.io/badge/React-20232a?style=flat-square&logo=react&logoColor=61DAFB)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)

</div>

**CodeSage AI** is an AI-powered repository analysis tool that helps developers understand unfamiliar codebases through natural language.

Instead of manually searching through hundreds of files or deciding which code snippets to provide to an AI assistant, users simply paste a GitHub repository URL. CodeSage AI automatically clones the repository, analyzes its source code, builds a semantic index, and answers repository-specific questions using Retrieval-Augmented Generation (RAG).

---

## Features

- Analyze any public GitHub repository using its URL
- Parse Python source code using the Abstract Syntax Tree (AST)
- Automatically extract classes and functions
- Split large source files into manageable chunks
- Generate embeddings using Ollama
- Retrieve the most relevant code using cosine similarity
- Expand retrieved chunks to include complete implementations
- Multi-turn repository-aware conversations
- Avoid rescanning repositories that have already been indexed
- React frontend for repository analysis and AI chat

---

## Tech Stack

| Layer    | Stack |
|----------|-------|
| Backend  | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) Requests |
| AI       | ![Ollama](https://img.shields.io/badge/Ollama-1a1a1a?style=flat-square&logo=ollama&logoColor=white) Qwen 2.5 3B, Nomic Embed Text, Retrieval-Augmented Generation (RAG) |
| Frontend | ![React](https://img.shields.io/badge/React-20232a?style=flat-square&logo=react&logoColor=61DAFB) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white) Axios, React Markdown |

---

## How It Works

```text
GitHub Repository URL
          │
          ▼
Clone Repository
          │
          ▼
Find Python Files
          │
          ▼
AST Parsing
          │
          ▼
Extract Classes & Functions
          │
          ▼
Chunk Source Code
          │
          ▼
Generate Embeddings
          │
          ▼
Semantic Retrieval
          │
          ▼
Context Expansion
          │
          ▼
Qwen 2.5
          │
          ▼
Repository-Specific Answer
```

---

## Project Structure

```text
codesage-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── engines/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/codesage-ai.git
cd codesage-ai
```

**2. Backend**

```bash
cd backend

python -m venv .venv
source .venv/bin/activate      # macOS/Linux

pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

**3. Install Ollama models**

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

Start Ollama:

```bash
ollama serve
```

**4. Frontend**

```bash
cd frontend

npm install
npm run dev
```

---

## Usage

1. Launch the backend.
2. Launch the frontend.
3. Paste a GitHub repository URL.
4. Click **Scan**.
5. Ask repository-specific questions, for example:

   > Explain the Session class.
   >
   > How does it manage cookies?

---

## Key Components

- **Repository Scanner** — clones a GitHub repository locally.
- **AST Parser** — extracts Python classes and functions from the repository.
- **Chunk Builder** — splits large source files into smaller chunks suitable for embedding.
- **Embedding Engine** — generates vector embeddings using the Nomic Embed Text model.
- **Retriever** — finds the most relevant code using cosine similarity.
- **Context Expansion** — automatically includes all parts of a retrieved class or function to improve answer quality.
- **AI Engine** — uses Qwen 2.5 with repository context to generate grounded answers.

---

## Motivation

General AI assistants require developers to decide which files or code snippets to provide as context.

Nobody enjoys reading someone else's codebase for the first time. CodeSage AI doesn't make the code more interesting — it just gets you to the interesting parts faster, by automatically analyzing the repository, retrieving the relevant source code, and supplying the appropriate context before generating an answer. Less time managing context, more time understanding the code.

---

## What's Next

- Repository explorer
- Read-only code viewer
- File-level navigation
- Multi-repository support
- Persistent sessions
- Vector database integration
- Streaming AI responses
- Support for additional programming languages