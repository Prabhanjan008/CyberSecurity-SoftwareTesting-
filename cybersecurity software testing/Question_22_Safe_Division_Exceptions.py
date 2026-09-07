"""
==============================================================================
QUESTION 22: Safe Division Exception Handling
==============================================================================
Description:
Write a Python program to accept a number from the user and perform a division 
operation, using exception handling to manage invalid (non-numeric) input and 
division-by-zero errors.
==============================================================================
"""

def safe_division():
    print("=== QUESTION 22: SAFE DIVISION EXCEPTION HANDLING ===")
    user_input = input("Enter a number to divide 100 by: ").strip()

    try:
        num = int(user_input)
        result = 100 / num
        print(f"\n[RESULT] 100 / {num} = {result}")
    except ValueError:
        print("\n[ERROR] Please enter a valid integer.")
    except ZeroDivisionError:
        print("\n[ERROR] Number cannot be zero.")

if __name__ == "__main__":
    safe_division()
