"""
LLM Fallback task — handles any question that no other task could answer.
This should always be registered LAST, so it acts as a catch-all.
"""
from llm_tool import ask_llm


def can_handle(question):
    # This task can handle literally anything — it's the fallback.
    return True


def run(question, context):
    return ask_llm(question)