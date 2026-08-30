import re

def parse(text):

    text = text.lower().strip()

    # -------------------------
    # FILE OPEN
    # -------------------------

    patterns = [

        r"open (.+)",
        r"read (.+)",
        r"show (.+)",
        r"display (.+)",
        r"load (.+)",
        r"can you open (.+)",
        r"can you read (.+)",
        r"please open (.+)",
        r"please read (.+)"
    ]

    for p in patterns:

        m = re.search(p, text)

        if m:
            obj = m.group(1)
            remove_words = [
                "my",
                "the",
                "a",
                "an",
                "pdf",
                "document",
                "file",
                "notes"
            ]

            remove_words = [
                "my",
                "the",
                "a",
                "an",
                "pdf",
                "document",
                "file",
                "notes",
                "latest",
                "last",
                "today",
                "it",
                "that",
                "this"
            ]

            words = obj.split()
            words = [w for w in words if w not in remove_words]

            obj = " ".join(words)
            obj = obj.replace(".pdf", "").strip()

            return {
                "intent":"file_read",
                "object":obj
            }

    return None