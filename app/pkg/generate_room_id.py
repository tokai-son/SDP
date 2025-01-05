import random
import string

# Generate a random 7 character long string
def generate_random_id():
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(7))
    return random_id
