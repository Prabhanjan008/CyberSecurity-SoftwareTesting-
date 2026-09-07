"""
==============================================================================
QUESTION 25: Secure File Deletion with Path Traversal Protection
==============================================================================
Description:
Write a Python program to securely delete a file from a designated uploads 
directory, but only after verifying that the resolved file path lies within 
that directory, in order to prevent path traversal attacks.
==============================================================================
"""
from pathlib import Path

def secure_delete():
    print("=== QUESTION 25: SECURE FILE DELETION ===")
    base_dir = Path("uploads").resolve()
    base_dir.mkdir(exist_ok=True)

    filename = input("Enter filename to delete from uploads: ").strip()
    file_path = (base_dir / filename).resolve()

    if base_dir in file_path.parents and file_path.is_file():
        file_path.unlink()
        print(f"\n[SUCCESS] Deleted '{filename}'.")
    else:
        print("\n[DENIED] Access denied or file does not exist.")

if __name__ == "__main__":
    secure_delete()
