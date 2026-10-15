import os
from dotenv import load_dotenv
from groq import Groq

import os as _os
_env_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(prompt, system_prompt="You are a helpful assistant."):
    """
    Calls the Groq API and returns the response.
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
    Summarizes the given text.
    """
    prompt = f"Summarize the following text clearly and concisely:\n\n{text}"
    return ask_llm(prompt, system_prompt="You are an expert summarizer. Give clear, concise summaries.")

def answer_question(document_text, question):
    """
    Answers the user's question based on the given document content.
    """
    prompt = f"""You are answering a question based on the following document.
Only use information from the document below. If the answer isn't in the document, say so clearly.

DOCUMENT:
{document_text}

QUESTION:
{question}

ANSWER:"""
    return ask_llm(prompt, system_prompt="You are a helpful assistant that answers questions strictly based on the provided document content.")    

import json as _json

def break_into_steps(goal_text):
    """
    Uses the LLM to break a complex goal into a list of simple,
    executable command strings (matching MyAI's existing command style).
    Returns a Python list of strings.
    """
    prompt = f"""Break the following user goal into a numbered list of simple, sequential steps.
Each step should be phrased as a short, direct command (like "readpdf filename.pdf" or "summarize it" or "sqrt 25").
Only output the steps, one per line, numbered like "1. ...". Do not add explanations.

GOAL: {goal_text}
"""
    response = ask_llm(prompt, system_prompt="You are a task planner. Break goals into simple, executable steps only.")

    steps = []
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        # remove leading "1. " / "1) " style numbering
        import re
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line)
        if cleaned:
            steps.append(cleaned)

    return steps    

_chat_history = []
MAX_HISTORY_MESSAGES = 8

CHAT_SYSTEM_PROMPT = (
    "You are MyAI, a helpful assistant. Keep answers short and direct unless the user asks for detail. "
    "Use the earlier conversation to understand follow-up questions such as 'and about France?'. "
    "If a question is too unclear to answer, ask one short clarifying question."
)


def chat_llm(question):
    """Chat with short-term memory: the last few turns are sent along with each question."""
    messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
    messages += _chat_history
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return f"LLM error: {str(e)}"

    _chat_history.append({"role": "user", "content": question})
    _chat_history.append({"role": "assistant", "content": answer})
    del _chat_history[:-MAX_HISTORY_MESSAGES]
    return answer    