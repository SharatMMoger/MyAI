TASKS = {}

def register(name, func):
    TASKS[name] = func

def run(name, *args):
    if name in TASKS:
        return TASKS[name](*args)
    return None