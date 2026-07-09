import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from rag import index_paper, get_indexed_papers, retrieve_relevant_chunks, build_context
from prompts import RAG_SYSTEM_PROMPT

# Read environment files safely
load_dotenv()

app = FastAPI(title="Research Knowledge Base API Layer")

# Activate Cross-Origin Mapping explicitly to allow Vite Dev servers on 5173 to interact seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize production Groq Client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("CRITICAL RECOVERY FAULT: Environment missing valid GROQ_API_KEY tokens.")
groq_client = Groq(api_key=api_key)

# Establish scratch upload staging paths securely
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class AskRequest(BaseModel):
    question: str
    paper_filter: str = None


@app.get("/health")
def health_check():
    """Confirms systemic routing is alive and kicking."""
    return {"status": "operational", "engine": "FastAPI + ChromaDB"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Receives file, parses layout blocks, and registers structures inside the vector database."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid format. Pipeline strictly limits inputs to PDF documents.")

    saved_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        # Stream file parts safely down onto disk
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger internal parsing routines
        chunk_count = index_paper(saved_path, file.filename)
        
        return {
            "status": "Success",
            "filename": file.filename,
            "chunks_indexed": chunk_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Processing Subsystem Failure: {str(e)}")
    finally:
        # Clean up temporary disk files immediately to prevent storage leaks
        if os.path.exists(saved_path):
            os.remove(saved_path)


@app.get("/papers")
def list_papers():
    """Fetches list of all documents indexed."""
    try:
        return {"papers": get_indexed_papers()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
def query_knowledge_base(payload: AskRequest):
    """Performs semantic search, structures the prompt, and queries Groq under zero-temperature rules."""
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Query prompt cannot be empty.")

    try:
        # 1. Fetch relevant text vectors based on query semantic profile
        matched_chunks = retrieve_relevant_chunks(
            query=payload.question,
            k=4,
            source_filter=payload.paper_filter
        )
        
        # 2. Honest fallback interception: return early if index contains no evidence
        if not matched_chunks:
            return {
                "answer": "I could not find any relevant information inside the uploaded papers.",
                "sources": [],
                "debug_chunks": []
            }

        # 3. Assemble isolated context boundary structures
        context_string = build_context(matched_chunks)

        # 4. Construct message payload
        messages = [
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": f"CONTEXT BLOCK:\n{context_string}\n\nUSER QUESTION: {payload.question}"}
        ]

        # 5. Query Groq via their official llama-3.3-70b production module
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.0  # Zero temperature eliminates hallucinations and forces facts
        )

        # 6. Extract raw unique source references to show along the UI track
        unique_sources = list(set([f"{c['source']} (Page {c['page_number']})" for c in matched_chunks]))

        return {
            "answer": completion.choices[0].message.content,
            "sources": unique_sources,
            "debug_chunks": matched_chunks  # Essential diagnostics tracking metric for debugging
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Failure: {str(e)}")