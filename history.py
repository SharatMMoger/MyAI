def save_history(question):

    with open("history.txt", "a", encoding="utf-8") as file:
        file.write(question + "\n")


def load_history():

    try:
        with open("history.txt", "r", encoding="utf-8") as file:
            return file.read()

    except:
        return "No history found."