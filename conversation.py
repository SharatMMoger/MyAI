import conversation_memory

def chat(question):

    q = question.lower()

    if q in ["hello", "hi", "hey"]:
        conversation_memory.set_topic("greeting")
        return "Hello!"

    if q == "how are you":
        conversation_memory.set_topic("greeting")
        return "I'm doing great."

    if q == "who are you":
        conversation_memory.set_topic("identity")
        return "I am MyAI."

    if q == "thank you":
        return "You're welcome!"

    if q == "bye":
        return "Goodbye!"

    return None