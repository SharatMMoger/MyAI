"""
RAG task: index a folder of documents, search them, and answer questions from them.
Commands:
    index [folder]         index the documents folder (or the given folder)
    search <query>         show the most relevant chunks
    docs ask <question>    answer from the indexed documents, with sources
"""
import rag_chain
import rag_store

FAILURE_PREFIXES = ("no matching", "no documents are indexed", "usage:", "rag error")


def can_handle(question):
    q = question.lower().strip()
    return (
        q == "index" or q.startswith("index ")
        or q.startswith("search ")
        or q == "docs ask" or q.startswith("docs ask ")
    )


def _handle(question):
    q = question.strip()
    low = q.lower()

    if low == "index" or low.startswith("index "):
        folder = q[6:].strip() or rag_store.DOCS_DIR
        summary = rag_store.index_folder(folder)
        msg = f"Indexed {summary['files']} file(s) with {summary['chunks']} chunk(s)."
        if summary["removed"]:
            msg += f" Removed {summary['removed']} stale chunk(s) from deleted files."
        if summary["skipped"]:
            msg += " Skipped: " + ", ".join(summary["skipped"])
        return msg

    if low.startswith("search "):
        docs = rag_store.search(q[7:].strip(), k=3)
        if not docs:
            return "No matching chunks above the similarity threshold."
        return "\n\n".join(
            f"[{d.metadata['source']}, chunk {d.metadata['chunk']}]\n{d.page_content[:200]}"
            for d in docs
        )

    if low == "docs ask" or low.startswith("docs ask "):
        question_text = q[8:].strip()
        if not question_text:
            return "Usage: docs ask <question>"
        return rag_chain.answer(question_text)

    return None


def run(question, context):
    try:
        return _handle(question)
    except Exception as e:
        return f"RAG error: {e}"


def verify(question, result):
    text = str(result).strip().lower()
    if not text:
        return False
    return not text.startswith(FAILURE_PREFIXES)