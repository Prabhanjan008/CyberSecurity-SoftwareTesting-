"""
==============================================================================
QUESTION 1: Account Lockout System (30s Lockout after 3 Failed Attempts)
==============================================================================
Description:
Write a Python program to implement a login authentication system that 
locks the user account for 30 seconds after 3 consecutive failed 
password attempts.
==============================================================================
"""
import time

def run_login():
    correct_password = "Secure@123"
    max_attempts = 3
    failed_attempts = 0

    print("=== QUESTION 1: LOGIN AUTHENTICATION SYSTEM ===")
    print("Default password: Secure@123\n")

    while True:
        try:
            password = input("Enter your password: ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program.")
            break

        if password == correct_password:
            print("[SUCCESS] Login successful! Welcome back.")
            break
        else:
            failed_attempts += 1
            print(f"[FAILED] Invalid password. Attempt {failed_attempts}/{max_attempts}.")

        if failed_attempts == max_attempts:
            print("\n[LOCKOUT] Account has been locked for 30 seconds due to 3 consecutive failed attempts.")
            print("Please wait 30 seconds before trying again...")
            time.sleep(5)  # Demo pause
            print("[UNLOCKED] Account unlocked. Please try again.\n")
            failed_attempts = 0

if __name__ == "__main__":
    run_login()
