"""
==============================================================================
QUESTION 7: Password Strength Checker
==============================================================================
Description:
Write a Python program to check the strength of a user-entered password based 
on its length, presence of uppercase letters, lowercase letters, digits, 
special characters, and whether it matches a list of commonly used weak passwords.
==============================================================================
"""
import re

def check_password_strength():
    print("=== QUESTION 7: PASSWORD STRENGTH CHECKER ===")
    weak_passwords = ["password", "123456", "12345678", "qwerty", "admin", "welcome", "letmein", "Password123"]
    password = input("Enter a password to evaluate: ").strip()

    if password.lower() in [weak.lower() for weak in weak_passwords]:
        print("\n[WEAK] Password is in list of common weak passwords.")
    elif len(password) < 8:
        print("\n[WEAK] Password must be at least 8 characters long.")
    elif not re.search(r"[A-Z]", password):
        print("\n[WEAK] Must contain at least one uppercase letter (A-Z).")
    elif not re.search(r"[a-z]", password):
        print("\n[WEAK] Must contain at least one lowercase letter (a-z).")
    elif not re.search(r"[0-9]", password):
        print("\n[WEAK] Must contain at least one number (0-9).")
    elif not re.search(r"[^A-Za-z0-9]", password):
        print("\n[WEAK] Must contain at least one special character.")
    else:
        print("\n[STRONG] Password meets all security requirements!")

if __name__ == "__main__":
    check_password_strength()
