<div align="center"> 

# 📄 RAG Document Assistant.  

**Upload PDFs → Ask Questions → Get AI-Powered Answers with Source Citations**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🧠 What Is This?

A **fully local, production-grade RAG (Retrieval-Augmented Generation)** application that lets you have intelligent conversations with your PDF documents — no cloud, no API keys, no data leaving your machine.

Built with **Ollama** (local LLMs), **ChromaDB** (vector storage), **LangChain** (orchestration), **FastAPI** (backend), and **Streamlit** (frontend). Includes a built-in **RAGAS evaluation pipeline** to measure answer quality.

---

## ✨ | Features |

- 📤 **PDF Upload** — drag-and-drop any PDF document
- 💬 **Semantic Q&A** — ask natural language questions, get context-aware answers
- 🔍 **Source Citations** — every answer shows which document chunks it came from
- 📊 **RAGAS Evaluation** — measure faithfulness, relevancy, and answer correctness
- 🔒 **100% Local** — runs entirely on your machine via Ollama; nothing sent to the cloud
- 🐳 **One-Command Setup** — Docker Compose spins up all 4 services automatically

---

## 🏗️ Architecture |

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│          (Upload · Ask Questions · Evaluate)            │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP
┌───────────────────────▼─────────────────────────────────┐
│                  FastAPI Backend                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ /upload  │  │  /chat   │  │    /evaluation        │  │
│  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘  │
│       │              │                   │              │
│  PDF Loader    RAG Pipeline           RAGAS             │
│  Chunker       LangChain Chain        Evaluator         │
└───┬────────────────┬───────────────────────────────────┘
    │                │
┌───▼────┐    ┌──────▼───────────────────────────────────┐
│ChromaDB│    │           Ollama (Local LLM)              │
│Vector  │    │    llama3 (chat) + nomic-embed-text       │
│Store   │    │              (embeddings)                  │
└────────┘    └──────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack||

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Ollama + llama3 | Local language model for Q&A |
| **Embeddings** | nomic-embed-text | Semantic vector embeddings |
| **Vector DB** | ChromaDB | Storing and searching document chunks |
| **Orchestration** | LangChain | RAG chain + retrieval |
| **Backend** | FastAPI | REST API + business logic |
| **Frontend** | Streamlit | Interactive web UI |
| **Evaluation** | RAGAS | Answer quality metrics |
| **Packaging** | Docker + Docker Compose | One-command deployment |

---

## ⚡ Quick Start 

### Prerequisites

- **Docker Desktop** — [download here](https://www.docker.com/products/docker-desktop/)
- **8 GB RAM** free (llama3 is ~4.7 GB)
- **10 GB disk space** free

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-document-assistant.git
cd rag-document-assistant
```

### 2. Start everything (PowerShell — Recommended)

```powershell
# Allow script execution (one-time setup)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Start all services
.\start.ps1
```

On the **first run**, the script will:
- Build all Docker images
- Pull Ollama models (`llama3` + `nomic-embed-text`) — takes **5–10 minutes**
- Start all services

### 3. Or start manually 

```bash
docker compose up --build -d
```

---

## 🌐 Access the Application

| Service | URL | Description |
|---|---|---|
| **Streamlit UI** | http://localhost:8501 | Main application interface |
| **FastAPI Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Ollama API** | http://localhost:11434 | Local LLM server |

---

## 📖 How to Use

1. Open **http://localhost:8501**
2. **Upload Document tab** → upload any PDF (research papers, reports, manuals, books)
3. **Ask Questions tab** → type any question about the document
4. **Evaluate tab** → run RAGAS metrics to measure answer quality

---

## 📁 Project Structure

```
rag-document-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── upload.py        # PDF upload endpoint
│   │   │   ├── chat.py          # Q&A endpoint
│   │   │   └── evaluation.py    # RAGAS evaluation endpoint
│   │   ├── core/
│   │   │   ├── config.py        # Settings & environment variables
│   │   │   ├── embeddings.py    # Ollama embeddings setup
│   │   │   ├── llm.py           # Ollama LLM setup
│   │   │   └── vectordb.py      # ChromaDB operations
│   │   ├── services/
│   │   │   ├── pdf_loader.py    # PDF text extraction
│   │   │   ├── chunker.py       # Text splitting (1000 chars, 200 overlap)
│   │   │   ├── rag_pipeline.py  # LangChain RAG chain
│   │   │   └── evaluator.py     # RAGAS evaluation logic
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   └── main.py              # FastAPI app entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── streamlit_app.py         # Streamlit UI (Upload · Chat · Evaluate)
│   ├── requirements.txt
│   └── Dockerfile
├── datasets/
│   └── eval_dataset.json        # Sample RAGAS evaluation dataset
├── docker-compose.yml           # All 4 services defined here
├── .env                         # Environment variables
├── start.ps1                    # One-click start (PowerShell)
├── stop.ps1                     # One-click stop (PowerShell)
└── README.md
```

---

## 🔌 API Reference

### Upload a PDF
```http
POST /upload/
Content-Type: multipart/form-data

file: <your-pdf-file>
```

### Ask a Question
```http
POST /chat/
Content-Type: application/json

{
  "question": "What are the key findings?"
}
```

**Response:**
```json
{
  "answer": "The key findings include...",
  "source_documents": ["chunk 1 text...", "chunk 2 text..."]
}
```

### Run RAGAS Evaluation
```http
POST /evaluation/
Content-Type: application/json

{
  "questions": ["What is RAG?"],
  "answers": ["RAG is Retrieval-Augmented Generation."],
  "contexts": [["RAG combines retrieval and generation..."]],
  "ground_truths": ["RAG stands for Retrieval-Augmented Generation."]
}
```

### Run Demo Evaluation
```http
GET /evaluation/demo
```

---

## ⚙️ Configuration

All settings live in `.env` and are loaded via Pydantic:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://ollama:11434` | Ollama server URL |
| `LLM_MODEL` | `llama3` | Chat model name |
| `EMBED_MODEL` | `nomic-embed-text` | Embedding model name |
| `CHUNK_SIZE` | `1000` | Characters per document chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `RETRIEVER_K` | `4` | Number of chunks retrieved per query |
| `CHROMA_DB_DIR` | `chroma_db` | Vector database directory |
| `UPLOAD_DIR` | `uploads` | PDF upload directory |

---

## 🐳 Docker Commands||

```powershell
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f ollama-pull

# Stop all services
.\stop.ps1
# or
docker compose down

# Rebuild after code changes
docker compose up --build -d

# Full reset (clears uploaded PDFs and vector DB)
docker compose down -v
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| Models not downloading | Run `docker compose logs -f ollama-pull` and wait — first pull takes 5–10 min |
| Backend not starting | Run `docker compose logs -f backend` and check for Python errors |
| "ChromaDB empty" error | Upload a PDF first via the Streamlit UI before asking questions |
| Out of memory | Close other apps — llama3 needs ~8 GB RAM |
| Port already in use | Edit port numbers in `docker-compose.yml` |
| PowerShell script blocked | Run: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| Frontend can't reach backend | Wait 30–60 seconds after startup for health checks to pass |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ using FastAPI · LangChain · ChromaDB · Ollama · RAGAS · Streamlit

</div>
