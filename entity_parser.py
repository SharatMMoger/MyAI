import re

def extract(text):

    text = text.lower()

    data = {
        "intent": None,
        "action": None,
        "subject": None,
        "file_type": None,
        "time": None
    }

    # ---------- Actions ----------

    if any(x in text for x in ["open", "read", "show", "display", "load"]):
        data["action"] = "open"

    elif any(x in text for x in ["find", "search", "locate"]):
        data["action"] = "find"

    # ---------- Subjects ----------

    subjects = [
        "cn",
        "java",
        "python",
        "resume",
        "notes",
        "ai"
    ]

    for s in subjects:
        if s in text:
            data["subject"] = s
            break

    # ---------- File Types ----------

    if "pdf" in text:
        data["file_type"] = "pdf"

    elif "excel" in text:
        data["file_type"] = "excel"

    elif "docx" in text:
        data["file_type"] = "docx"

    elif "ppt" in text:
        data["file_type"] = "ppt"

    # ---------- Time ----------

    if "latest" in text:
        data["time"] = "latest"

    elif "last" in text:
        data["time"] = "last"

    elif "today" in text:
        data["time"] = "today"

    return data