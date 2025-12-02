import os
import json
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

RAG_DIR = "rag"
os.makedirs(RAG_DIR, exist_ok=True)

INDEX_PATH = os.path.join(RAG_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(RAG_DIR, "chunks.json")
META_PATH = os.path.join(RAG_DIR, "metadata.json")

model = SentenceTransformer("all-MiniLM-L6-v2") 


def load_faiss_index(dim=384):
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    idx = faiss.IndexFlatL2(dim)
    return idx


def load_chunks():
    if not os.path.exists(CHUNKS_PATH):
        return []
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata():
    if not os.path.exists(META_PATH):
        return []
    with open(META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_chunks(chunks):
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)


def save_metadata(meta):
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def chunk_text(text, chunk_size=500):
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


def process_pdf_for_faiss(document_id, file_path):    
    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            full_text += extracted + "\n"

    chunks = chunk_text(full_text)

    embeddings = model.encode(chunks).astype("float32")

    index = load_faiss_index(dim=embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    all_chunks = load_chunks()
    chunk_start_index = len(all_chunks)
    all_chunks.extend(chunks)
    save_chunks(all_chunks)

    meta = load_metadata()
    meta.append({
        "document_id": document_id,
        "start": chunk_start_index,
        "end": chunk_start_index + len(chunks)
    })
    save_metadata(meta)

    return len(chunks)
