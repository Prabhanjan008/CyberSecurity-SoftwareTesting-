"""
==============================================================================
QUESTION 36: JWT Authorization Policy Enforcement (Issuer, Audience, Role, Scope)
==============================================================================
Security Features Implemented:
1. Token generation with 'iss', 'aud', 'sub', 'role', 'scope', 'iat', and 'exp'.
2. Strict verification of signature, expiration, issuer, and audience using PyJWT.
3. Fine-grained RBAC (Role-Based Access Control) & Scope validation.
4. Non-disclosing generic error messages ("Access denied") to prevent details leakage.
==============================================================================
"""

import jwt
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

SECRET_KEY = "my-super-secret-key-at-least-32-bytes-long!"
ALGORITHM = "HS256"

# Authorization policy
AUTHORIZATION_POLICY = {
    "issuer": "https://example.com",
    "audience": "my-api",
    "required_role": "admin",
    "required_scope": "read:users"
}


# ---------------------------------------------------------
# Create JWT
# ---------------------------------------------------------

def create_token():
    now = datetime.now(timezone.utc)

    payload = {
        "sub": "user123",
        "iss": "https://example.com",
        "aud": "my-api",
        "role": "admin",
        "scope": "read:users write:users",
        "iat": now,
        "exp": now + timedelta(minutes=10)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ---------------------------------------------------------
# Validate JWT and Authorization Policy
# ---------------------------------------------------------

def validate_token(token):
    try:
        # Verify signature, expiration, issuer and audience
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=AUTHORIZATION_POLICY["issuer"],
            audience=AUTHORIZATION_POLICY["audience"]
        )

        # Check required role
        if decoded.get("role") != AUTHORIZATION_POLICY["required_role"]:
            return False, "Access denied"

        # Check required scope
        scopes = decoded.get("scope", "").split()

        if AUTHORIZATION_POLICY["required_scope"] not in scopes:
            return False, "Access denied"

        return True, decoded

    except jwt.ExpiredSignatureError:
        return False, "Access denied"

    except jwt.InvalidIssuerError:
        return False, "Access denied"

    except jwt.InvalidAudienceError:
        return False, "Access denied"

    except jwt.InvalidTokenError:
        return False, "Access denied"


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    # Generate a JWT
    token = create_token()

    print("Generated JWT:")
    print(token)

    print("\nValidating JWT against authorization policy...")

    valid, result = validate_token(token)

    if valid:
        print("\nACCESS GRANTED")
        print("User:", result["sub"])
        print("Role:", result["role"])
        print("Scope:", result["scope"])
    else:
        print("\nACCESS DENIED")
        print("Reason:", result)
