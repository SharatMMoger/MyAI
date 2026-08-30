import re

INTENTS = {

    "greet": [
        "hello", "hi", "hey", "good morning",
        "good afternoon", "good evening",
        "how are you", "hiya", "yo", "greetings"
    ],

    "history": [
        "history",
        "show history",
        "conversation history",
        "chat history",
        "previous conversation"
    ],

    "memory": [
        "remember",
        "what is my",
        "who am i",
        "do you remember",
        "my name",
        "my city",
        "last question",
        "last answer",
        "last topic",
        "last command",
        "repeat",
        "repeat last answer"
    ],

    "calculator": [

        "+", "-", "*", "/",

        "plus",
        "minus",
        "times",
        "divided",

        "add",
        "sum",
        "subtract",
        "multiply",
        "divide",

        "square",
        "squared",
        "cube",
        "cubed",

        "sqrt",
        "square root",
        "cube root",

        "power",
        "raised",

        "calculate",
        "percentage",

        "factorial",
        "gcd",
        "lcm",

        "mean",
        "median",
        "mode",
        "variance",
        "stddev",

        "probability",
        "ncr",
        "npr"
    ],

    "file_search": [
        "find",
        "search",
        "locate",
        "where is",
        "search for",
        "find file",
        "find pdf",
        "find document"
    ],

    "file_read": [
        "read",
        "readpdf",
        "readexcel",
        "readdocx",
        "readppt",

        "open",
        "show",
        "display",
        "load",

        "open pdf",
        "read pdf",
        "open document",
        "show pdf"
    ],

    "file_list": [
        "list files",
        "show files",
        "display files"
    ],

    "help": [
        "help",
        "commands",
        "what can you do"
    ]
}


def detect_intent(text):

    text = text.lower().strip()

    # Direct math expression
    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", text):
        return "calculator"

    priority = [
        "calculator",
        "file_read",
        "file_search",
        "memory",
        "history",
        "file_list",
        "help",
        "greet"
    ]

    for intent in priority:

        for word in INTENTS[intent]:

            # Symbols (+ - * /)
            if word in ["+", "-", "*", "/"]:
                if word in text:
                    return intent
                continue

            # Exact word / phrase match
            pattern = r"\b" + re.escape(word) + r"\b"

            if re.search(pattern, text):
                return intent

    return "unknown"