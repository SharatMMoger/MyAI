def run(text):

    if not text:
        return "Nothing to summarize."

    lines = text.splitlines()

    lines = [line.strip() for line in lines if line.strip()]

    summary = "Summary:\n\n"

    for line in lines[:10]:
        summary += "- " + line + "\n"

    return summary