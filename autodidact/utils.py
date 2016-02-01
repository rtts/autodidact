import random

HUMAN_FRIENDLY_CHARS = "234679ABCDEFGHJKLMNPRSTUVWXYZabcdefghijkmnpqrstuvwxyz"

def random_string(length):
    return ''.join(random.choice(HUMAN_FRIENDLY_CHARS) for x in range(length))
