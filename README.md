# 📚 Research Knowledge Base (Enterprise RAG Pipeline)

An enterprise-grade **Retrieval-Augmented Generation (RAG)** application designed to query, analyze, and extract accurate insights from academic research papers.

The application combines a **React** frontend with a **FastAPI** backend, **ChromaDB** vector database, and **Groq LLM inference** to deliver fast, context-aware responses while minimizing AI hallucinations through strict retrieval guardrails.

---

# ✨ Features

- 📄 Upload and analyze academic research papers (PDF)
- 🔍 Semantic search powered by vector embeddings
- 🤖 Retrieval-Augmented Generation (RAG)
- ⚡ Ultra-fast LLM inference using Groq
- 📚 Source citations with page numbers
- 🛡️ Built-in hallucination prevention
- 🔒 Secure API key management using environment variables
- 🎨 Modern React + Tailwind CSS interface
- 💾 Persistent ChromaDB vector storage

---

# 🏗️ System Architecture

```text
               PDF Upload
                    │
                    ▼
          PDF Text Extraction
                    │
                    ▼
      Intelligent Text Chunking
                    │
                    ▼
          Embedding Generation
                    │
                    ▼
             ChromaDB Storage
                    │
             User Question
                    │
                    ▼
        Semantic Vector Search
                    │
                    ▼
      Relevant Context Retrieved
                    │
                    ▼
      Groq Large Language Model
                    │
                    ▼
      Grounded Answer + Citation
```

---

# 🧠 Core Concepts

## Retrieval-Augmented Generation (RAG)

Instead of relying solely on an LLM's pretrained knowledge, the system retrieves relevant document chunks and injects them into the model's prompt before generating an answer.

This enables:

- More accurate responses
- Domain-specific knowledge
- Reduced hallucinations
- Better explainability

---

## Semantic Vector Search

The application uses **ChromaDB** to store embeddings of document chunks.

Unlike traditional keyword search, semantic search understands the **meaning** behind a query and retrieves the most contextually relevant information.

---

## Hallucination Prevention

The pipeline includes strict safeguards to prevent fabricated answers.

If retrieved chunks fail to meet the required relevance threshold, the application refuses to answer and returns:

> **"I cannot find sufficient evidence in the document to answer your query safely."**

This ensures every response remains grounded in the uploaded document.

---

## Transparent Citations

Every generated answer includes:

- Source document
- Referenced text chunk
- Page number

This allows users to verify every generated response.

---

# 🚀 Tech Stack

## Backend

- Python 3.9+
- FastAPI
- Uvicorn

## Frontend

- React
- Vite
- Tailwind CSS

## AI & Vector Database

- ChromaDB
- Groq API
- Embedding Model

---

# 📋 Prerequisites

Install the following before running the project:

- Python 3.9+
- Node.js v18+
- npm
- Git
- Groq API Key

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/hassanbilal803-code/Research_knowledge_base.git

cd Research_knowledge_base
```

---

## 2. Backend Setup

Navigate to the backend folder.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file inside the **backend** directory.

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

> **Important:** Never commit your `.env` file to GitHub.

---

## 4. Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

Backend URL:

```
http://localhost:8000
```

---

## 5. Run the Frontend

Open a new terminal.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

Frontend URL:

```
http://localhost:5173
```

---

# 📂 Project Structure

```text
Research_knowledge_base/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   └── database/
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    │
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

---

# 💡 How It Works

### Step 1

Upload an academic research paper in PDF format.

↓

### Step 2

The backend:

- Extracts text
- Splits the document into chunks
- Generates embeddings
- Stores vectors in ChromaDB

↓

### Step 3

Ask questions about the paper.

Example:

> *What methodology was used to calculate the experimental error margins?*

↓

### Step 4

The application retrieves the most relevant chunks.

↓

### Step 5

The retrieved context is passed to the LLM.

↓

### Step 6

The model generates a grounded answer with citations.

---

# 🛡️ Production Guardrails

## Intelligent Chunking

Uses recursive character splitting with overlap to preserve context across chunk boundaries.

Benefits:

- Better retrieval
- Higher answer quality
- Reduced context fragmentation

---

## Anti-Hallucination Pipeline

If relevant context cannot be found, the model is **not allowed** to guess.

Instead, it returns a safe fallback response.

This prevents fabricated information from being generated.

---

## Session Isolation

Every uploaded document is tagged with unique metadata.

This ensures:

- No cross-document contamination
- Session-specific retrieval
- Clean vector searches

---

# 📷 Workflow

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Chunking
 │
 ▼
Embeddings
 │
 ▼
ChromaDB
 │
 ▼
Semantic Search
 │
 ▼
Retrieved Context
 │
 ▼
Groq LLM
 │
 ▼
Grounded Answer
 │
 ▼
Citation + Page Number
```

---

# 🛠️ Troubleshooting

## ModuleNotFoundError

Ensure the virtual environment is activated before installing dependencies.

```bash
source venv/bin/activate
```

or

```bash
venv\Scripts\activate
```

---

## HTTP 401 Unauthorized

Verify your `.env` file contains a valid Groq API key.

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

---

## SQLite Version Conflict

Some systems use an older SQLite version.

Install:

```bash
pip install pysqlite3-binary
```

Then apply the SQLite override in `main.py` if required.

---

# 🔮 Future Improvements

- Multi-document querying
- PDF highlighting
- OCR support
- Hybrid search (Keyword + Vector)
- User authentication
- Conversation memory
- Docker deployment
- Kubernetes support
- Cloud vector database integration
- Streaming LLM responses
- Admin dashboard
- Export chat history

---

# 👨‍💻 Author

**Hassan Bilal**

GitHub:

https://github.com/hassanbilal803-code

---


---

# 📄 License

This project is intended for educational, research, and portfolio purposes.

Feel free to use and modify the code with proper attribution.



