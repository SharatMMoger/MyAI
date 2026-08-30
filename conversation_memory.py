context = {}

def remember(key, value):
    context[key] = value

def recall(key):
    return context.get(key)

def clear():
    context.clear()

def all_context():
    return context

# ---------- New Functions ----------

def set_topic(topic):
    context["last_topic"] = topic

def get_topic():
    return context.get("last_topic")

def set_answer(answer):
    context["last_answer"] = answer

def get_answer():
    return context.get("last_answer")

def set_command(command):
    context["last_command"] = command

def get_command():
    return context.get("last_command")

def set_question(question):
    context["last_question"] = question

def get_question():
    return context.get("last_question")    