import random
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def getRandomCode():
    return random.randint(1000, 99999)

import hashlib

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def verify_token_validity(valid_token:str, token:str) -> bool:
    return valid_token == hash_token(token)

# app/utils/password_utils.py


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def display_members(members: list):
    all_members = []
    for member in members:
        memberInfo = {
            "name": member.name,
            "email": member.email,
        }
        all_members.append(memberInfo)

    return all_members
