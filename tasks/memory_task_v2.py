"""
Memory task — remembers and recalls simple facts (e.g., "remember my name is Sharat").
"""
from memory import save_memory, load_memory


def can_handle(question):
    q = question.lower().strip()
    return q.startswith("remember ") or q.startswith("what is ")


def run(question, context):
    q = question.strip()
    q_lower = q.lower()

    if q_lower.startswith("remember "):
        try:
            content = q[9:]
            key, value = content.split(" is ", 1)
            save_memory(key.strip().lower(), value.strip())
            return "I will remember that."
        except:
            return "Usage: remember my name is sharat"

    if q_lower.startswith("what is "):
        key = q[8:].strip().lower()
        memory = load_memory()
        if key in memory:
            return memory[key]
        return None  # let it fall through to LLM if not found

    return None