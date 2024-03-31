import random
def getRandomCode():
    return random.randint(1000, 99999)

import hashlib

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token_validity(valid_token:str, token:str) -> bool:
    return valid_token == hash_token(token)