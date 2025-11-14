import random
import string

def generate_4_char_code() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))
