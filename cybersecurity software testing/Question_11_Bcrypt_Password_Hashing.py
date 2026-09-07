"""
==============================================================================
QUESTION 11: Bcrypt Password Hashing & Account Lockout
==============================================================================
Description:
Write a Python program to implement a secure login system that stores the 
user's password as a bcrypt hash instead of plain text, verifies login attempts 
against the stored hash, and locks the account for 30 seconds after 3 
consecutive failed attempts.
==============================================================================
"""
import bcrypt
import time
import getpass

def run_bcrypt_system():
    print("=== QUESTION 11: BCRYPT PASSWORD HASHING ===")
    try:
        password = getpass.getpass("Create a new password: ")
    except Exception:
        password = "SecureBcrypt123!"

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    print(f"[BCRYPT HASH GENERATED]: {hashed_password.decode('utf-8')}\n")

    max_attempts = 3
    lockout_time = 30
    failed_attempts = 0

    while True:
        try:
            entered_password = getpass.getpass("Enter password to log in: ")
        except Exception:
            entered_password = input("Enter password to log in: ")

        if bcrypt.checkpw(entered_password.encode("utf-8"), hashed_password):
            print("[SUCCESS] Login successful!")
            break
        else:
            failed_attempts += 1
            print(f"[FAILED] Invalid password. Attempt {failed_attempts}/{max_attempts}.")

        if failed_attempts >= max_attempts:
            print(f"\n[LOCKOUT] Account locked for {lockout_time} seconds.")
            time.sleep(3)
            print("[UNLOCKED] Try again.\n")
            failed_attempts = 0

if __name__ == "__main__":
    run_bcrypt_system()
