### Text Proccesssing 
# CS 480: Database Systems
# Carmen A. Thom

import os
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

def get_chunked_text(chunk_size = 500):
    all_chunks = []

    for filename in os.listdir("dataset"):
        full_path = os.path.join("dataset", filename)

        reader = PdfReader(full_path)
        full_text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                full_text += extracted + "\n"

        chunks = [
            full_text[i:i + chunk_size] 
            for i in range(0, len(full_text), chunk_size)
        ]
        all_chunks.extend(chunks)

    return all_chunks

def get_embeddings():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = get_chunked_text()
    embeddings = model.encode(chunks, show_progress_bar=True)
    return chunks, embeddings

def index_faiss():
    chunks, embeddings = get_embeddings()

    embeddings = np.array(embeddings).astype("float32")
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, "vector_index.faiss")

    with open("chunks.txt", "w", encoding = "utf-8") as f:
        for c in chunks:
            c = c.replace("\n", " ") 
            f.write(c + "\n<<<END>>>\n")

def load_chunks():
    chunks = []
    buffer = ""

    with open("chunks.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "<<<END>>>":
                chunks.append(buffer.strip())
                buffer = ""
            else:
                buffer += line

    return chunks

def search_faiss(query, k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("vector_index.faiss")
    chunks = load_chunks()

    q_emb = model.encode([query]).astype("float32")
    D, I = index.search(q_emb, k)

    results = []
    for rank, (idx, dist) in enumerate(zip(I[0], D[0])):
        results.append({
            "rank": rank + 1,
            "chunk_index": int(idx),
            "distance": float(dist),
            "text": chunks[idx]
        })

    return results

def main():
    if not os.path.exists("vector_index.faiss"):
        index_faiss()
    results = search_faiss("How was the market in 2018?")
    for r in results:
        print(f"Result {r['rank']}")
        print(r["text"][:500], "\n---\n")


if __name__ == "__main__":
    main()
