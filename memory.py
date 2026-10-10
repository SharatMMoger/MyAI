import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_memory.json")


def load_memory():
    """Load all saved memory as a dictionary."""
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_memory(key, value):
    """Save or update a single fact in memory."""
    memory = load_memory()
    memory[key.strip().lower()] = value.strip()

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2, ensure_ascii=False)


def get_memory(key):
    """Retrieve a single fact by key."""
    memory = load_memory()
    return memory.get(key.strip().lower())


def forget_memory(key):
    """Remove a specific fact from memory."""
    memory = load_memory()
    key = key.strip().lower()
    if key in memory:
        del memory[key]
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(memory, file, indent=2, ensure_ascii=False)
        return True
    return False