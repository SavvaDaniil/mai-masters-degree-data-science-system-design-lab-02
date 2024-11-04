import random
import string

class RandomUtil:

    def get_random_string_only_numbers(length: int) -> str:
        letters = string.digits
        result_str: str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    def get_random_string(length: int) -> str:
        letters = string.ascii_lowercase
        result_str: str = ''.join(random.choice(letters) for i in range(length))
        return result_str