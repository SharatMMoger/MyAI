import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(prompt, system_prompt="You are a helpful assistant."):
    """
    Groq API ko call karta hai aur response return karta hai.
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"LLM error: {str(e)}"


def summarize_text(text):
    """
    Diya gaya text summarize karta hai.
    """
    prompt = f"Summarize the following text clearly and concisely:\n\n{text}"
    return ask_llm(prompt, system_prompt="You are an expert summarizer. Give clear, concise summaries.")

def answer_question(document_text, question):
    """
    Document ke content ke base pe user ke sawaal ka jawab deta hai.
    """
    prompt = f"""You are answering a question based on the following document.
Only use information from the document below. If the answer isn't in the document, say so clearly.

DOCUMENT:
{document_text}

QUESTION:
{question}

ANSWER:"""
    return ask_llm(prompt, system_prompt="You are a helpful assistant that answers questions strictly based on the provided document content.")    