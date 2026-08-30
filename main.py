from knowledge import knowledge
from brain import get_response

MEMORY_FILE = "memory text"

# Load saved memory
try:
    with open(MEMORY_FILE, "r") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                knowledge[key] = value
except:
    pass

print("Knowledge loaded:", len(knowledge))
print("Welcome to MyAI!")
print("Type 'exit' to quit.")

while True:

    question = input("Ask me something: ")

    if not question.strip():
        continue

    if question.lower() == "exit":
        print("Goodbye!")
        break

    print("MyAI:", get_response(question))