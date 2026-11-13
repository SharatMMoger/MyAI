"""
Grounded question answering over indexed documents.
Retrieves the chunks above the similarity threshold, then asks the Groq LLM
(through LangChain) to answer using only those chunks.
"""
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

import rag_store

# Load GROQ_API_KEY from src 1/.env, whatever folder this runs from
load_dotenv(os.path.join(rag_store.BASE_DIR, ".env"))

GROQ_MODEL = "openai/gpt-oss-120b"
TEMPERATURE = 0.7  # same as the plain ask command, so the paper's comparison is fair
MAX_TOKENS = 1024

NO_ANSWER = "The documents do not contain an answer to that question."

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You answer questions using only the document excerpts provided. "
     "If the excerpts do not contain the answer, say that the documents do not contain it. "
     "Do not guess and do not use outside knowledge."),
    ("human", "Document excerpts:\n{context}\n\nQuestion: {question}"),
])


def _format_context(docs):
    return "\n\n".join(
        f"[{d.metadata['source']}, chunk {d.metadata['chunk']}]\n{d.page_content}"
        for d in docs
    )


def answer(question, k=4):
    """Answers a question from the indexed documents and lists the sources used."""
    if rag_store.count() == 0:
        return "No documents are indexed yet. Run 'index' first."

    docs = rag_store.search(question, k=k)
    if not docs:
        # Nothing is relevant enough, so refuse without calling the LLM
        return NO_ANSWER

    llm = ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
    chain = PROMPT | llm | StrOutputParser()
    text = chain.invoke({"context": _format_context(docs), "question": question})

    sources = sorted({f"{d.metadata['source']} (chunk {d.metadata['chunk']})" for d in docs})
    return f"{text.strip()}\n\nSources: {', '.join(sources)}"


if __name__ == "__main__":
    print(answer("Who founded Zentra?"))
    print()
    print(answer("What is the capital of France?"))