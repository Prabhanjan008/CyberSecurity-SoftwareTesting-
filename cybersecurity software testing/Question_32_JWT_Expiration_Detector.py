"""
==============================================================================
QUESTION 32: Detect Expired JSON Web Tokens (JWTs)
==============================================================================
Description:
A Python program to detect expired JWTs. The program verifies the JWT 
signature and automatically rejects the token if its expiration time (exp) 
has passed. It displays clear messages indicating token status.
==============================================================================
"""
import time
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "my_secure_secret_key_1234567890123456"

def create_token(expiration_seconds=10):
    payload = {
        "user": "student",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expiration_seconds)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("[VALID] JWT is valid.")
        print("User:", payload.get("user"))
        return True
    except ExpiredSignatureError:
        print("[EXPIRED] JWT has expired. Access denied.")
        return False
    except InvalidTokenError as e:
        print(f"[INVALID] Invalid JWT. Access denied. ({e})")
        return False

if __name__ == "__main__":
    print("=== QUESTION 32: JWT Expiration Detection Demo ===\n")
    token = create_token(expiration_seconds=5)
    print("Generated JWT:\n", token)

    print("\n1. Validating JWT immediately:")
    validate_token(token)

    print("\n2. Waiting 6 seconds for token to expire...")
    time.sleep(6)

    print("\n3. Validating JWT after expiration:")
    validate_token(token)
