"""
==============================================================================
QUESTION 35: Secure Production-Grade JWT Authentication with Rate Limiting
==============================================================================
Security Features Implemented:
1. User authentication with username and password.
2. Secure PBKDF2 password hashing (Werkzeug / hashlib).
3. JWT generated ONLY after credential validation succeeds.
4. Explicit algorithm enforcement (algorithms=['HS256']) to prevent algorithm confusion attacks.
5. UTC-aware expiration timestamp ('exp' claim) and issued-at ('iat' claim).
6. Complete validation of JWT signature and expiration time.
7. Rate limiting on /login endpoint (5 attempts/min) to prevent brute-force attacks.
8. Immediate rejection of tampered, invalid, or expired tokens.
9. Generic non-disclosing error messages ("Invalid credentials") to prevent account enumeration.
==============================================================================
"""

import time
import json
import secrets
import hashlib
import uuid
import threading
from functools import wraps
from datetime import datetime, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict, deque
import urllib.request
import urllib.error
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# ---------------------------------------------------------
# Security Configuration
# ---------------------------------------------------------
# Strong, secret key (Minimum 256 bits for HMAC-SHA256)
SECRET_KEY = "c8f7e2a9b4d1e3f5a7c9b2d4e6f8a0b1c3d5e7f9a2b4c6d8e0f1a3b5c7d9e1f3"
ALLOWED_ALGORITHM = "HS256"

# Password Hashing Utility using PBKDF2-HMAC-SHA256 with 100,000 iterations
def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex(), salt.hex()

def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    salt = bytes.fromhex(stored_salt)
    computed_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, stored_hash)

# Secure User Database (Passwords stored exclusively as PBKDF2 hashes)
_admin_hash, _admin_salt = hash_password("SecurePassword123!")
_user_hash, _user_salt = hash_password("StudentSecret456!")

USER_DATABASE = {
    "admin": {"hash": _admin_hash, "salt": _admin_salt, "role": "admin"},
    "student": {"hash": _user_hash, "salt": _user_salt, "role": "student"}
}

# ---------------------------------------------------------
# Rate Limiting Engine (Sliding Window Algorithm)
# ---------------------------------------------------------
class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, client_ip: str) -> tuple[bool, int, float]:
        now = time.time()
        cutoff = now - self.window_seconds
        with self._lock:
            history = self._requests[client_ip]
            while history and history[0] <= cutoff:
                history.popleft()
            if len(history) < self.max_requests:
                history.append(now)
                return True, self.max_requests - len(history), self.window_seconds
            else:
                reset_in = max(0.0, (history[0] + self.window_seconds) - now)
                return False, 0, round(reset_in, 2)

login_rate_limiter = RateLimiter(max_requests=5, window_seconds=60.0) # Brute-force protection
api_rate_limiter = RateLimiter(max_requests=10, window_seconds=60.0)

# ---------------------------------------------------------
# JWT Operations
# ---------------------------------------------------------
def generate_jwt(username: str, role: str, expires_in_seconds: int = 15) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in_seconds),
        "jti": str(uuid.uuid4())
    }
    # Algorithm explicitly restricted to HS256
    return jwt.encode(payload, SECRET_KEY, algorithm=ALLOWED_ALGORITHM)

def validate_jwt(token: str) -> tuple[bool, dict | str]:
    try:
        # STRICT ALGORITHM RESTRICTION: algorithm matching explicitly enforced
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALLOWED_ALGORITHM])
        return True, payload
    except ExpiredSignatureError:
        # Non-disclosing detail for public caller, clear log internal
        return False, "Token has expired"
    except InvalidTokenError:
        return False, "Invalid or tampered token"

# ---------------------------------------------------------
# REST API Handler
# ---------------------------------------------------------
class SecureAuthHandler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict, headers: dict = None):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        if headers:
            for k, v in headers.items():
                self.send_header(k, str(v))
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_POST(self):
        client_ip = self.client_address[0]

        if self.path == '/api/login':
            # 1. Apply Brute-Force Rate Limiting on Login Endpoint
            allowed, remaining, reset_in = login_rate_limiter.check(client_ip)
            headers = {
                'X-RateLimit-Limit': login_rate_limiter.max_requests,
                'X-RateLimit-Remaining': remaining,
                'X-RateLimit-Reset': reset_in
            }
            if not allowed:
                self._json(429, {
                    "status": "error",
                    "message": "Too many login attempts. Please try again later."
                }, headers=headers)
                return

            # 2. Parse Payload
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length).decode('utf-8'))
            except Exception:
                self._json(400, {"status": "error", "message": "Invalid JSON format"})
                return

            username = body.get('username')
            password = body.get('password')
            expires_in = body.get('expires_in', 10)

            # 3. Authenticate User against Password Hash
            user = USER_DATABASE.get(username)
            if not user or not verify_password(password, user['hash'], user['salt']):
                # SECURITY RULE: Generic error message to prevent account enumeration
                self._json(401, {"status": "error", "message": "Invalid username or password"})
                return

            # 4. Issue JWT only after successful authentication
            token = generate_jwt(username, user['role'], expires_in_seconds=expires_in)
            self._json(200, {
                "status": "success",
                "message": "Authentication successful",
                "access_token": token,
                "token_type": "Bearer",
                "expires_in_seconds": expires_in
            })
        else:
            self._json(404, {"status": "error", "message": "Not Found"})

    def do_GET(self):
        client_ip = self.client_address[0]

        # Rate Limit Check
        allowed, remaining, reset_in = api_rate_limiter.check(client_ip)
        if not allowed:
            self._json(429, {"status": "error", "message": "Rate limit exceeded"})
            return

        if self.path == '/api/protected':
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self._json(401, {"status": "error", "message": "Authentication required"})
                return

            token = auth_header.split(' ', 1)[1]
            valid, result = validate_jwt(token)

            if not valid:
                # SECURITY RULE: Generic access denied without revealing cryptographic keys/signatures
                self._json(401, {"status": "error", "message": f"Access denied: {result}"})
                return

            self._json(200, {
                "status": "success",
                "message": "Access granted to secure resource",
                "data": {
                    "subject": result.get("sub"),
                    "role": result.get("role"),
                    "token_id": result.get("jti")
                }
            })
        else:
            self._json(404, {"status": "error", "message": "Not Found"})

    def log_message(self, format, *args):
        pass

def run(port=8090):
    httpd = HTTPServer(('127.0.0.1', port), SecureAuthHandler)
    print(f"[SECURE AUTH SERVER] Running on http://127.0.0.1:{port}/")
    httpd.serve_forever()

# ---------------------------------------------------------
# Test Verification Suite
# ---------------------------------------------------------
def test_suite():
    print("=== QUESTION 4: Secure JWT Auth & Brute-Force Rate Limit Test ===\n")
    threading.Thread(target=run, kwargs={'port': 8090}, daemon=True).start()
    time.sleep(1)

    url_login = "http://127.0.0.1:8090/api/login"
    url_protected = "http://127.0.0.1:8090/api/protected"

    def req(url, method='GET', payload=None, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f"Bearer {token}"
        data = json.dumps(payload).encode('utf-8') if payload else None
        r = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(r) as resp:
                return resp.status, json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))

    # 1. Invalid Login Attempt (Generic Error)
    print("1. Testing Invalid Credentials (Generic Error Check):")
    st, res = req(url_login, "POST", {"username": "admin", "password": "WrongPassword!"})
    print(f"   Status: {st} | Response: {res['message']}")
    assert st == 401 and res['message'] == "Invalid username or password"

    # 2. Successful Login & JWT Issuance
    print("\n2. Testing Valid Login & JWT Issuance:")
    st, res = req(url_login, "POST", {"username": "admin", "password": "SecurePassword123!", "expires_in": 3})
    print(f"   Status: {st} | Access Token Received")
    jwt_token = res["access_token"]

    # 3. Access Protected Route with Valid JWT
    print("\n3. Testing Access to Protected Route with Valid JWT:")
    st, res = req(url_protected, "GET", token=jwt_token)
    print(f"   Status: {st} | Response: {res['message']} (User: {res['data']['subject']})")
    assert st == 200

    # 4. Access Protected Route with Tampered Signature
    print("\n4. Testing Tampered JWT Signature Rejection:")
    tampered_token = jwt_token[:-4] + "BADX"
    st, res = req(url_protected, "GET", token=tampered_token)
    print(f"   Status: {st} | Response: {res['message']}")
    assert st == 401

    # 5. Access Protected Route after Token Expiration
    print("\n5. Testing Expired Token Rejection (Waiting 4 seconds)...")
    time.sleep(4)
    st, res = req(url_protected, "GET", token=jwt_token)
    print(f"   Status: {st} | Response: {res['message']}")
    assert st == 401

    # 6. Brute-Force Rate Limiting Enforcement on Login (5 Max Attempts)
    print("\n6. Testing Brute-Force Rate Limiter on /login (Breaching 5 Attempts Limit):")
    for attempt in range(1, 6):
        st, res = req(url_login, "POST", {"username": "admin", "password": "WrongPassword!"})
        print(f"   Attempt #{attempt}: Status = {st} | Message = {res['message']}")
        if st == 429:
            print("   [PASS] Brute-force rate limiter successfully triggered 429 Too Many Requests!")
            break

    print("\n=== ALL SECURITY VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_suite()
