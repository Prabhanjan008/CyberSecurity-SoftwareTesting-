"""
==============================================================================
QUESTION 6: Multi-Factor Authentication (MFA with PyOTP)
==============================================================================
Description:
Write a Python program to implement multi-factor authentication (MFA) using a 
password as the first factor and a Time-based One-Time Password (TOTP), 
generated using the pyotp library, as the second factor.
==============================================================================
"""
import pyotp

def run_mfa():
    print("=== QUESTION 6: MULTI-FACTOR AUTHENTICATION (MFA) ===")
    correct_password = "Python123"
    secret_key = "JBSWY3DPEHPK3PXP"
    totp = pyotp.TOTP(secret_key)

    print(f"Secret Key: {secret_key}")
    print(f"[CURRENT TOTP TOKEN]: {totp.now()}\n")

    password = input("Step 1: Enter your password: ")

    if password == correct_password:
        print("[SUCCESS] Password verified!")
        otp = input("Step 2: Enter the 6-digit OTP from authenticator app: ").strip()
        if totp.verify(otp):
            print("\n[SUCCESS] MFA authentication successful! Access granted.")
        else:
            print("\n[DENIED] Invalid OTP code.")
    else:
        print("\n[DENIED] Invalid password.")

if __name__ == "__main__":
    run_mfa()
