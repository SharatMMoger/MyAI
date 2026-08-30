import os
import difflib

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def search_file(keyword):

    keyword = keyword.lower()

    files = []

    for root, dirs, filenames in os.walk(PROJECT_FOLDER):
        for file in filenames:
            files.append(file)

    # Exact Match
    exact = [f for f in files if keyword in f.lower()]

    if exact:
        return exact

    # Fuzzy Match
    matches = difflib.get_close_matches(
        keyword,
        [f.lower() for f in files],
        n=5,
        cutoff=0.35
    )

    result = []

    for m in matches:
        for f in files:
            if f.lower() == m:
                result.append(f)

    return result