from passlib.context import CryptContext

context = CryptContext(schemes=["argon2"])

def hash_password(password_hash:str):
    return context.hash(password_hash)

def verify_password(password_hash:str, password2:str):
    return context.verify(password_hash, password2)