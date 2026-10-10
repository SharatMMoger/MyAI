"""
Progress task — shows task completion statistics, recent history, and allows reset.
"""
import task_tracker


def can_handle(question):
    q = question.lower().strip()
    return q in ["progress", "show progress", "task status", "stats", "reset progress", "task history"]


def run(question, context):
    q = question.lower().strip()

    if q == "reset progress":
        task_tracker.reset_history()
        return "Task history has been reset."

    if q == "task history":
        history = task_tracker.get_recent_history(10)
        if not history:
            return "No task history yet."
        lines = []
        for h in history:
            lines.append(f"[{h['status']}] {h['task']} — \"{h['question']}\"")
        return "Recent Task History:\n" + "\n".join(lines)

    # default: progress stats
    stats = task_tracker.get_progress()
    bar_length = 20
    filled = int((stats["percentage"] / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    return (
        f"Task Progress\n"
        f"Completed: {stats['completed']}\n"
        f"Failed: {stats['failed']}\n"
        f"Total: {stats['total']}\n\n"
        f"{bar} {stats['percentage']}%"
    )