import random
import string


def generate_code(length: int = 7):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
