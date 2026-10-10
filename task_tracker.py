"""
Task Tracker — records status of every dispatched task (PENDING, RUNNING, COMPLETED, FAILED)
and provides progress statistics.
"""
import json
import os
from datetime import datetime

TRACKER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "task_history.json")


def _load_history():
    if not os.path.exists(TRACKER_FILE):
        return []
    try:
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def _save_history(history):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def log_task(task_name, question, status, error=None):
    """
    Records a task execution event.
    status: "RUNNING", "COMPLETED", "FAILED"
    """
    history = _load_history()
    history.append({
        "task": task_name,
        "question": question,
        "status": status,
        "error": error,
        "timestamp": datetime.now().isoformat()
    })
    _save_history(history)


def get_progress():
    """
    Returns a summary: completed, failed, total, and percentage.
    """
    history = _load_history()
    total = len(history)
    completed = sum(1 for h in history if h["status"] == "COMPLETED")
    failed = sum(1 for h in history if h["status"] == "FAILED")

    percentage = round((completed / total) * 100, 1) if total > 0 else 0

    return {
        "total": total,
        "completed": completed,
        "failed": failed,
        "percentage": percentage
    }


def get_recent_history(limit=10):
    """Returns the most recent N task events."""
    history = _load_history()
    return history[-limit:]

def reset_history():
    """Clears all task history."""
    _save_history([])