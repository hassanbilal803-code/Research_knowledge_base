# backend/rag.py
import os
import re
import fitz  # PyMuPDF
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize persistent ChromaDB local disk workspace
DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma_db"))
chroma_client = chromadb.PersistentClient(path=DB_DIR)

# Create or fetch unified vector collection table
collection = chroma_client.get_or_create_collection(name="research_papers")

# Initialize open-source 384-dimensional text encoder model at the module level
print("Loading sentence-transformers/all-MiniLM-L6-v2...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
print("Embedding model successfully cached in system memory.")


def extract_text_from_pdf(pdf_path: str) -> list:
    """
    Layout-aware extractor: parses academic two-column text sequences 
    while attaching strict page numbers and metadata.
    """
    doc = fitz.open(pdf_path)
    filename = os.path.basename(pdf_path)
    extracted_pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        width = page.rect.width
        height = page.rect.height
        
        # Strip out typical top/bottom margin areas where headers and footers pollute data
        header_limit = height * 0.08
        footer_limit = height * 0.92
        midline = width / 2

        blocks = page.get_text("blocks")
        left_col = []
        right_col = []

        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            if block_type != 0 or y0 < header_limit or y1 > footer_limit:
                continue
            
            # Divide content across page layout columns
            if x0 < midline:
                left_col.append((y0, text))
            else:
                right_col.append((y0, text))

        # Order blocks from top to bottom
        left_col.sort(key=lambda x: x[0])
        right_col.sort(key=lambda x: x[0])

        # Merge text blocks natively according to proper human reading order
        page_text = "\n".join([t[1] for t in left_col] + [t[1] for t in right_col])
        
        extracted_pages.append({
            "text": page_text,
            "page_number": page_num + 1
        })
        
    doc.close()
    return extracted_pages


def clean_text(text: str) -> str:
    """Cleans extracted raw text blocks of messy layout spacing artifact patterns."""
    # Collapse consecutive space characters down into single entities
    text = re.sub(r'[ \t]+', ' ', text)
    # Wipe out single orphan standalone lines that just indicate isolated digits/page marks
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.M)
    # Standardize multiple consecutive line break spikes into clean double returns
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 400, overlap: int = 60) -> list:
    """Splits text sequences down by paragraph groupings without exceeding word boundaries."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_word_count = 0

    for para in paragraphs:
        para_words = para.split(" ")
        # If a single paragraph is massive, break it sequentially
        if len(para_words) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
            for i in range(0, len(para_words), chunk_size - overlap):
                slice_words = para_words[i:i + chunk_size]
                chunks.append(" ".join(slice_words))
            continue

        if current_word_count + len(para_words) > chunk_size:
            chunks.append(" ".join(current_chunk))
            # Include basic trailing overlap history tracking markers
            overlap_words = current_chunk[-overlap:] if len(current_chunk) >= overlap else current_chunk
            current_chunk = list(overlap_words) + para_words
            current_word_count = len(current_chunk)
        else:
            current_chunk.extend(para_words)
            current_word_count += len(para_words)

    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return [c for c in chunks if c.strip()]


def index_paper(pdf_path: str, paper_name: str) -> int:
    """Ingests, cleans, chunks, vectorizes, and indexes document payloads into ChromaDB."""
    raw_pages = extract_text_from_pdf(pdf_path)
    
    documents = []
    metadatas = []
    ids = []
    
    chunk_idx = 0
    for page in raw_pages:
        cleaned = clean_text(page["text"])
        page_chunks = chunk_text(cleaned)
        
        for chunk in page_chunks:
            documents.append(chunk)
            metadatas.append({
                "source": paper_name,         # Required for strict catalog filtering
                "page_number": page["page_number"]
            })
            ids.append(f"{paper_name}_chunk_{chunk_idx}")
            chunk_idx += 1

    if not documents:
        return 0

    # Generate layout vector footprints via a single optimized batch execution
    embeddings = embedder.encode(documents).tolist()

    # Commit records directly onto the persistent storage volume
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    return len(documents)


def get_indexed_papers() -> list:
    """Queries ChromaDB metadata layers to return all unique parsed document labels."""
    results = collection.get(include=["metadatas"])
    if not results or not results.get('metadatas'):
        return []
    # Deduplicate source titles across collections
    unique_papers = list(set([meta['source'] for meta in results['metadatas'] if 'source' in meta]))
    return sorted(unique_papers)


def retrieve_relevant_chunks(query: str, k: int = 4, source_filter: str = None) -> list:
    """Executes semantic cosine distance indexing to fetch context references."""
    query_vector = embedder.encode([query]).tolist()
    
    # Configure precise search isolation constraints
    search_kwargs = {"query_embeddings": query_vector, "n_results": k}
    if source_filter:
        search_kwargs["where"] = {"source": source_filter}

    results = collection.query(**search_kwargs)
    
    formatted_results = []
    docs = results.get('documents', [[]])[0]
    metas = results.get('metadatas', [[]])[0]
    distances = results.get('distances', [[]])[0]

    for i in range(len(docs)):
        # Calculate real-time vector distance relevance quality profiles
        score = distances[i] if i < len(distances) else 0.0
        # Print logs in the background for real-time development inspection
        print(f"[RETR LOG] Match Index: {i} | Distance Match Delta: {score:.4f} | File Reference: {metas[i]['source']}")
        
        formatted_results.append({
            "text": docs[i],
            "source": metas[i]["source"],
            "page_number": metas[i]["page_number"],
            "distance": score
        })
    return formatted_results


def build_context(chunks: list) -> str:
    """Formats retrieved list segments into explicit contextual boundaries."""
    context_blocks = []
    for idx, chunk in enumerate(chunks):
        block = f"[Source {idx + 1}: {chunk['source']} (Page {chunk['page_number']})]\n{chunk['text']}"
        context_blocks.append(block)
    return "\n\n".join(context_blocks)