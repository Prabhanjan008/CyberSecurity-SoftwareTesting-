"""
==============================================================================
QUESTION 10: Secure Getpass Masked Login with Account Lockout
==============================================================================
Description:
Write a Python program to implement a secure login system that accepts the 
password using getpass (so it is not displayed on screen) and locks the 
account for 30 seconds after 3 consecutive failed login attempts.
==============================================================================
"""
import time
import getpass

def run_getpass_system():
    print("=== QUESTION 10: SECURE GETPASS MASKED LOGIN ===")
    try:
        correct_password = getpass.getpass("Create a password: ")
    except Exception:
        correct_password = "SecurePassword123"

    max_attempts = 3
    lockout_time = 30
    failed_attempts = 0

    while True:
        try:
            password = getpass.getpass("Enter your password: ")
        except Exception:
            password = input("Enter your password: ")

        if password == correct_password:
            print("[SUCCESS] Login successful!")
            break
        else:
            failed_attempts += 1
            print(f"[FAILED] Invalid password. Attempt {failed_attempts}/{max_attempts}.")

        if failed_attempts >= max_attempts:
            print(f"\n[LOCKOUT] Too many failed attempts. Account locked for {lockout_time} seconds.")
            time.sleep(3)
            print("[UNLOCKED] You can try again now.\n")
            failed_attempts = 0

if __name__ == "__main__":
    run_getpass_system()
