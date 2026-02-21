import hashlib
import bcrypt
from typing import Optional

def hash_md5(password: str) -> str:
    """Simulate MD5 hashing (for educational purposes only)"""
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha256(password: str) -> str:
    """Simulate SHA256 hashing (for educational purposes only)"""
    return hashlib.sha256(password.encode()).hexdigest()

def hash_bcrypt(password: str) -> str:
    """Simulate bcrypt hashing (for educational purposes only)"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_hash(password: str, hash_value: str, hash_type: str) -> bool:
    """Verify a password against a hash (simulation only)"""
    if hash_type == "MD5":
        return hash_md5(password) == hash_value
    elif hash_type == "SHA256":
        return hash_sha256(password) == hash_value
    elif hash_type == "bcrypt":
        return bcrypt.checkpw(password.encode(), hash_value.encode())
    return False
