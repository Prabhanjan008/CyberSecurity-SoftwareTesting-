"""
==============================================================================
QUESTION 5: Dictionary-Based Password Attack Simulation
==============================================================================
Description:
Write a Python program to simulate a dictionary-based password attack by 
testing a list of common passwords against a stored password, and display the 
password and the number of attempts once it is found.
==============================================================================
"""

def dictionary_attack_sim():
    print("=== QUESTION 5: DICTIONARY-BASED PASSWORD ATTACK SIMULATION ===")
    correct_password = "Python123"
    password_list = ["admin", "password", "123456", "welcome", "Python", "Python123", "qwerty"]

    attempts = 0
    found = False

    for password in password_list:
        attempts += 1
        print(f"Attempt #{attempts}: Trying password '{password}'...")
        if password == correct_password:
            print("\n[CRACKED] Password found!")
            print(f"Password : {password}")
            print(f"Attempts : {attempts}")
            found = True
            break

    if not found:
        print("\n[FAILED] Password was not found in dictionary list.")

if __name__ == "__main__":
    dictionary_attack_sim()
