"""
==============================================================================
QUESTION 26: Secure File Creation inside Uploads Directory
==============================================================================
Description:
Write a Python program to securely create a new file inside a designated 
uploads directory, but only after verifying that the resolved file path remains 
within that directory, in order to prevent path traversal attacks.
==============================================================================
"""
from pathlib import Path

def secure_create():
    print("=== QUESTION 26: SECURE FILE CREATION ===")
    base_dir = Path("uploads").resolve()
    base_dir.mkdir(exist_ok=True)

    filename = input("Enter filename to create: ").strip()
    file_path = (base_dir / filename).resolve()

    if base_dir in file_path.parents:
        file_path.touch()
        print(f"\n[SUCCESS] File created at: {file_path}")
    else:
        print("\n[DENIED] Access denied! File outside uploads.")

if __name__ == "__main__":
    secure_create()
