from difflib import get_close_matches

def best_match(word, choices):

    matches = get_close_matches(
        word,
        choices,
        n=1,
        cutoff=0.6
    )

    if matches:
        return matches[0]

    return None