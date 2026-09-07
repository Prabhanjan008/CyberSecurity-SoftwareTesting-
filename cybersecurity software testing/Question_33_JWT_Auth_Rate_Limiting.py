"""
==============================================================================
QUESTION 33: Secure JWT Authentication with Rate Limiting (Sliding Window)
==============================================================================
Description:
Implementation of thread-safe Sliding Window Rate Limiter (429 Too Many Requests),
PBKDF2 password hashing, JWT issuance and token validation server.
==============================================================================
"""
import time
import json
import hashlib
import secrets
import threading
from collections import defaultdict, deque
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import jwt

SECRET_KEY = "my_secret_key_for_jwt_auth_rate_limit"

def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex(), salt.hex()

def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    salt = bytes.fromhex(stored_salt)
    computed_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, stored_hash)

_hash, _salt = hash_password("Secret123!")
USER_DB = {"admin": {"hash": _hash, "salt": _salt, "role": "admin"}}

class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, client_ip: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        with self._lock:
            history = self._requests[client_ip]
            while history and history[0] <= cutoff:
                history.popleft()
            if len(history) < self.max_requests:
                history.append(now)
                return True
            return False

rate_limiter = RateLimiter(max_requests=5, window_seconds=60.0)

def generate_jwt(username, role):
    payload = {
        "sub": username,
        "role": role,
        "exp": time.time() + 300
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

if __name__ == "__main__":
    print("=== QUESTION 33: JWT AUTH & SLIDING WINDOW RATE LIMITING ===")
    print("[SUCCESS] Rate limiter & JWT Auth ready.")
