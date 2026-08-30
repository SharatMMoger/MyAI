SYNONYMS = {

    "cn": [
        "computer network",
        "computer networks",
        "network",
        "networking",
        "cn"
    ],

    "java": [
        "java",
        "java programming",
        "programming"
    ],

    "resume": [
        "resume",
        "cv",
        "curriculum vitae"
    ],

    "pdf": [
        "pdf",
        "document"
    ]

}


def normalize(text):

    text = text.lower()

    for key, values in SYNONYMS.items():

        for value in values:

            if value in text:

                text = text.replace(value, key)

    return text