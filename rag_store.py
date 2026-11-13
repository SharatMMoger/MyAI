"""
Document store for RAG: reads files from the documents folder, splits them into
chunks, embeds the chunks, and saves them in a persistent Chroma database.
The database always mirrors the folder that was last indexed.
"""
import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import file_tools

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION = "myai_docs_cosine"  # new name: the distance metric changed
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MIN_SCORE = 0.15 # cosine similarity; placeholder until calibrated
SUPPORTED = (".pdf", ".txt", ".docx")

_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
_store = None

CALIBRATION_QUERIES = [
    "Who founded Zentra?",
    "How many trucks does the fleet have?",
    "What is the course name?",
    "What is the capital of France?",
    "Recipe for chocolate cake",
]


def _get_store():
    """Creates the Chroma store on first use, then reuses it. Uses cosine distance."""
    global _store
    if _store is None:
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        _store = Chroma(
            collection_name=COLLECTION,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
            collection_metadata={"hnsw:space": "cosine"},
        )
    return _store


def count():
    """Number of chunks in the database."""
    return len(_get_store().get()["ids"])


def _read_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return file_tools.read_pdf(path)
    if ext == ".docx":
        return file_tools.read_docx(path)
    return file_tools.read_file(path)


def _delete_chunks_of(name):
    """Removes all stored chunks that came from this file name."""
    store = _get_store()
    old = store.get(where={"source": name})
    if old["ids"]:
        store.delete(ids=old["ids"])


def index_file(path):
    """Re-indexes one file: old chunks are removed first. Returns the new chunk count."""
    name = os.path.basename(path)
    _delete_chunks_of(name)

    text = _read_text(path)
    if not text or text.startswith("PDF Error"):
        return 0

    chunks = _splitter.split_text(text.replace("\ufeff", ""))  # BOM from Windows UTF-8 files
    if not chunks:
        return 0

    docs = [
        Document(page_content=chunk, metadata={"source": name, "chunk": i})
        for i, chunk in enumerate(chunks)
    ]
    ids = [f"{name}::{i}" for i in range(len(docs))]
    _get_store().add_documents(docs, ids=ids)
    return len(docs)


def _remove_stale(current_names):
    """Removes chunks whose source file is no longer in the folder. Returns the count."""
    store = _get_store()
    everything = store.get(include=["metadatas"])
    stale = [
        chunk_id
        for chunk_id, meta in zip(everything["ids"], everything["metadatas"])
        if meta.get("source") not in current_names
    ]
    if stale:
        store.delete(ids=stale)
    return len(stale)


def index_folder(folder=DOCS_DIR):
    """
    Makes the database match this folder: indexes every supported file and
    removes chunks of files that are no longer there.
    """
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")

    summary = {"files": 0, "chunks": 0, "skipped": [], "removed": 0}
    current = set()
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith(SUPPORTED):
            continue
        current.add(name)
        count_new = index_file(os.path.join(folder, name))
        if count_new:
            summary["files"] += 1
            summary["chunks"] += count_new
        else:
            summary["skipped"].append(name)

    summary["removed"] = _remove_stale(current)
    return summary


def search_with_scores(query, k=4):
    """Returns (chunk, cosine similarity) pairs, best first. Chroma gives distance = 1 - similarity."""
    results = _get_store().similarity_search_with_score(query, k=k)
    return [(doc, 1.0 - distance) for doc, distance in results]


def search(query, k=4, min_score=MIN_SCORE):
    """Returns the top-k chunks whose similarity is at least min_score."""
    return [doc for doc, score in search_with_scores(query, k=k) if score >= min_score]


if __name__ == "__main__":
    print("Indexed:", index_folder())
    print("Total chunks in database:", count())
    print()
    for q in CALIBRATION_QUERIES:
        print(f"Q: {q}")
        for doc, score in search_with_scores(q, k=2):
            print(f"   {score:.3f}  {doc.metadata['source']} (chunk {doc.metadata['chunk']})")
        print()