"""
==============================================================================
QUESTION 30: Generic Non-Disclosing Exception Handling
==============================================================================
Description:
Write a Python program to demonstrate safe exception handling for a division 
operation performed on user input, ensuring that internal technical error details 
are never exposed to the user.
==============================================================================
"""

def safe_calc():
    print("====================================")
    print(" Safe Calculation Program")
    print("====================================")
    try:
        val = input("Enter a number: ").strip()
        num = int(val)
        res = 100 / num
        print(f"Result: {res}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    except Exception:
        print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    safe_calc()
