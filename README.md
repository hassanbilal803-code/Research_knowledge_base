# 📚 Research Knowledge Base (RAG Pipeline)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF4F00?style=for-the-badge&logo=database&logoColor=white)

An enterprise-grade Retrieval-Augmented Generation (RAG) architecture engineered to query, analyze, and extract precise insights from dense academic research papers. This full-stack application pairs a dynamic React frontend with a high-performance FastAPI backend to deliver highly accurate, context-aware answers while strictly preventing AI hallucinations.

## 🧠 Core Concepts & System Architecture

This project demonstrates the advanced implementation of several critical AI and backend systems engineering concepts:

*   **Retrieval-Augmented Generation (RAG):** Bypasses the knowledge cutoff of standard Large Language Models (LLMs) by injecting dynamically retrieved, highly relevant document context directly into the AI's prompt space prior to generation.
*   **Semantic Vector Search:** Utilizes ChromaDB to convert text chunks into high-dimensional embeddings. This allows the system to retrieve information based on underlying mathematical meaning and context, rather than relying on rigid keyword matching.
*   **Strict Hallucination Guardrails:** Built-in fallback interception prevents the AI from guessing or fabricating information. If the vector database returns irrelevant chunks, the LLM is explicitly instructed to refuse to answer, and the UI dynamically hides the citation tray.
*   **Transparent Sourcing:** Every successful AI response is paired with a specific document citation and page number, ensuring all extracted data is traceable and verifiable.
*   **Secure Secrets Management:** Implements robust environment variable isolation (`.env` vs `.env.example`) to ensure API keys remain strictly local, protecting against accidental commits and automated GitHub secret scanning.

## 🛠️ Tech Stack

*   **Backend Interface:** Python, FastAPI, Uvicorn
*   **Client / Frontend:** ReactJS
*   **Vector Database:** ChromaDB (Local SQLite implementation)
*   **LLM Inference Engine:** Groq API (Optimized for ultra-low latency generation)

---

## 📋 Prerequisites

Before setting up the project, ensure your local machine has the following installed:
*   **Python 3.9+** (For the backend server)
*   **Node.js & npm** (For the frontend client)
*   **Git** (For version control and cloning)
*   A valid **Groq API Key** (For LLM inference)

---

## ⚙️ Local Setup & Installation

Follow these step-by-step instructions to get the development environment running on your local machine.

### 1. Clone the Repository
Begin by pulling the codebase to your local machine and navigating into the project folder.
```bash
git clone [https://github.com/hassanbilal803-code/Research_knowledge_base.git](https://github.com/hassanbilal803-code/Research_knowledge_base.git)
cd Research_knowledge_base