"""
==============================================================================
QUESTION 23: Reject Absolute Paths
==============================================================================
Description:
Write a Python program to accept a file path from the user and reject the path 
if it is an absolute path, allowing only relative paths.
==============================================================================
"""
import os

def check_relative_path():
    print("=== QUESTION 23: REJECT ABSOLUTE PATHS ===")
    path = input("Enter a file path: ").strip()

    if os.path.isabs(path):
        print(f"\n[DENIED] Absolute paths are not allowed: {path}")
    else:
        print(f"\n[ACCEPTED] Relative path accepted: {path}")

if __name__ == "__main__":
    check_relative_path()
