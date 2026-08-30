MEMORY_FILE = "user_memory.txt"


def save_memory(key, value):
    with open(MEMORY_FILE, "a") as file:
        file.write(f"{key}={value}\n")


def load_memory():
    memory = {}

    try:
        with open(MEMORY_FILE, "r") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)

                memory[key] = value

    except FileNotFoundError:
        pass

    return memory