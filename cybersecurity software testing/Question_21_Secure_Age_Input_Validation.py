"""
==============================================================================
QUESTION 21: Secure Age Input Validation
==============================================================================
Description:
Write a Python program to securely validate a user-entered age by checking 
for empty input, excessive input length, non-numeric characters, and a valid 
age range (1 to 120).
==============================================================================
"""

def validate_age():
    print("=== QUESTION 21: SECURE AGE INPUT VALIDATION ===")
    age_str = input("Enter your age: ").strip()

    if not age_str:
        print("\n[ERROR] Age input cannot be empty.")
    elif len(age_str) > 3:
        print("\n[ERROR] Input length too long (max 3 digits).")
    elif not age_str.isdigit():
        print("\n[ERROR] Age must contain digits only.")
    else:
        age = int(age_str)
        if age < 1 or age > 120:
            print("\n[ERROR] Age must be between 1 and 120.")
        else:
            print(f"\n[VALIDATED] Valid age accepted: {age}")

if __name__ == "__main__":
    validate_age()
