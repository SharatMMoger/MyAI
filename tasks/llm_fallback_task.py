"""
LLM Fallback task: handles any question no other task could answer.
Always registered LAST. Uses chat history so follow-up questions work.
"""
from llm_tool import chat_llm


def can_handle(question):
    return True


def run(question, context):
    return chat_llm(question)