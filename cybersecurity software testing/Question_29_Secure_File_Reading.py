"""
==============================================================================
QUESTION 29: Secure File Reading from Uploads Directory
==============================================================================
Description:
Write a Python program to securely open and display the contents of a file 
from a designated uploads directory, but only after verifying that the resolved 
file path lies within that directory, in order to prevent path traversal attacks.
==============================================================================
"""
from pathlib import Path

def secure_read():
    print("=== QUESTION 29: SECURE FILE READ ===")
    base_dir = Path("uploads").resolve()
    base_dir.mkdir(exist_ok=True)

    demo = base_dir / "readable.txt"
    demo.write_text("Hello! This is secure file content inside uploads directory.")

    filename = input("Enter filename to read: ").strip()
    file_path = (base_dir / filename).resolve()

    if base_dir in file_path.parents and file_path.is_file():
        print("\n[CONTENTS]:\n")
        with open(file_path, "r") as f:
            print(f.read())
    else:
        print("\n[ACCESS DENIED] File not found or outside directory.")

if __name__ == "__main__":
    secure_read()
