"""
==============================================================================
QUESTION 28: Directory Boundary Check using pathlib relative_to()
==============================================================================
Description:
Write a Python program to accept a filename from the user and use the 
pathlib relative_to() method to verify that the resulting file path lies 
within a designated documents directory before granting access to it.
==============================================================================
"""
from pathlib import Path

def check_relative_to():
    print("=== QUESTION 28: PATHLIB relative_to() CHECK ===")
    base_dir = Path("documents").resolve()
    base_dir.mkdir(exist_ok=True)

    filename = input("Enter filename: ").strip()
    req = (base_dir / filename).resolve()

    try:
        rel = req.relative_to(base_dir)
        print(f"\n[ACCESS ALLOWED] File inside documents directory: {rel}")
    except ValueError:
        print("\n[ACCESS DENIED] Path traversal detected!")

if __name__ == "__main__":
    check_relative_to()
