"""
Goal task — breaks a complex request into steps, executes each via the dispatcher,
verifies results, and reports overall progress.
"""
from llm_tool import break_into_steps
import dispatcher
import task_tracker


def can_handle(question):
    q = question.lower().strip()
    return q.startswith("goal:") or q.startswith("goal ")


def run(question, context):
    goal_text = question.split(":", 1)[-1].strip() if ":" in question else question[5:].strip()

    steps = break_into_steps(goal_text)
    if not steps:
        return "Could not break this goal into steps. Try rephrasing it."

    report_lines = [f"Goal: {goal_text}\n"]
    completed_count = 0
    last_output = None

    for i, step in enumerate(steps, start=1):
        result = dispatcher.dispatch(step, context)

        history = task_tracker.get_recent_history(1)
        status = history[-1]["status"] if history else "FAILED"

        if result and status == "COMPLETED":
            report_lines.append(f"Step {i}: {step} → COMPLETED")
            completed_count += 1
            last_output = result
        else:
            report_lines.append(f"Step {i}: {step} → FAILED")
            skipped = len(steps) - i
            if skipped > 0:
                report_lines.append(f"Stopped: {skipped} remaining step(s) skipped.")
            break

    total = len(steps)
    percentage = round((completed_count / total) * 100, 1)
    report_lines.append(f"\nGoal Status: {completed_count}/{total} steps completed ({percentage}%)")

    if last_output and completed_count == total:
        report_lines.append(f"\nFinal Output:\n{last_output}")

    return "\n".join(report_lines)