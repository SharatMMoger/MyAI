"""
Memory task: remembers and recalls simple facts (e.g. "remember my name is Sharat").
Only claims "what is ..." questions when the key actually exists in memory.
"""
from memory import save_memory, load_memory


def can_handle(question):
    q = question.lower().strip()
    if q.startswith("remember "):
        return True
    if q.startswith("what is "):
        return q[8:].strip() in load_memory()
    return False


def run(question, context):
    q = question.strip()
    q_lower = q.lower()

    if q_lower.startswith("remember "):
        try:
            content = q[9:]
            key, value = content.split(" is ", 1)
            save_memory(key.strip().lower(), value.strip())
            return "I will remember that."
        except ValueError:
            return "Usage: remember my name is sharat"

    if q_lower.startswith("what is "):
        return load_memory().get(q_lower[8:].strip())

    return None