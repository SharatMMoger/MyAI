state = {

    "last_file": None,

    "last_answer": None,

    "last_search": None,

    "last_topic": None,

    "last_intent": None

}


def set_value(key, value):
    state[key] = value


def get_value(key):
    return state.get(key)


def clear():

    for key in state:

        state[key] = None