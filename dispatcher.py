"""
Central task registry and dispatcher.
Now includes status tracking and basic retry logic.
"""
FAILURE_INDICATORS = [
    "invalid", "error", "usage:", "no matching", "not found",
    "no file has been opened", "sorry, i couldn't", "i'm not sure"
]


def _looks_like_failure(result):
    """
    Heuristic check: does this result look like an error/failure message
    rather than a genuine successful answer?
    """
    if not result:
        return True
    result_lower = str(result).lower()
    return any(indicator in result_lower for indicator in FAILURE_INDICATORS)

import task_tracker

TASKS = []
MAX_RETRIES = 1  # how many times to retry a failed task


def register(name, can_handle, run, verify=None):
    """
    verify (optional): function(question, result) -> True/False
    If provided, this is used instead of the generic failure heuristic
    to decide whether the task's result counts as a genuine success.
    """
    TASKS.append({
        "name": name,
        "can_handle": can_handle,
        "run": run,
        "verify": verify
    })


def dispatch(question, context=None):
    if context is None:
        context = {}

    for task in TASKS:
        try:
            if task["can_handle"](question):
                return _run_with_tracking(task, question, context)
        except Exception as e:
            print(f"[Dispatcher] Task '{task['name']}' matching failed: {e}")
            continue

    return None


def _run_with_tracking(task, question, context):
    name = task["name"]
    attempts = 0

    while attempts <= MAX_RETRIES:
        attempts += 1
        task_tracker.log_task(name, question, "RUNNING")

        try:
            result = task["run"](question, context)
            verify_fn = task.get("verify")

            if verify_fn:
                is_success = result and verify_fn(question, result)
            else:
                is_success = result and not _looks_like_failure(result)

            if is_success:
                task_tracker.log_task(name, question, "COMPLETED")
                return result
            elif result:
                task_tracker.log_task(name, question, "FAILED", error=result[:100])
                return result
            else:
                task_tracker.log_task(name, question, "FAILED", error="Empty result")

        except Exception as e:
            task_tracker.log_task(name, question, "FAILED", error=str(e))

        if attempts <= MAX_RETRIES:
            print(f"[Dispatcher] Retrying task '{name}' (attempt {attempts + 1})...")

    return None