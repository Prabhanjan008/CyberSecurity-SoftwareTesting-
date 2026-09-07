"""
==============================================================================
QUESTION 19: Directory Path Validation & Secure Listing
==============================================================================
Description:
Write a Python program to validate a user-entered directory path and securely 
display its contents using subprocess, preventing command injection attacks.
==============================================================================
"""
import os
import subprocess

def list_directory():
    print("=== QUESTION 19: DIRECTORY PATH VALIDATION ===")
    directory = input("Enter directory path: ").strip()

    if not os.path.isdir(directory):
        print("\n[ERROR] Directory path does not exist!")
    else:
        try:
            cmd = ["dir", directory] if os.name == 'nt' else ["ls", directory]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=(os.name=='nt'))
            print("\n[CONTENTS]:\n", res.stdout[:500])
        except subprocess.CalledProcessError:
            print("\n[ERROR] Failed to list directory contents.")

if __name__ == "__main__":
    list_directory()
