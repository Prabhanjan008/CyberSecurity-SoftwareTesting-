"""
==============================================================================
QUESTION 24: Pathlib Upload Validation (.txt extension check)
==============================================================================
Description:
Write a Python program to accept a filename from the user and allow access to 
it only if the resolved file path lies within a designated uploads directory 
and has a .txt extension, in order to prevent path traversal attacks.
==============================================================================
"""
from pathlib import Path

def validate_txt_file():
    print("=== QUESTION 24: PATHLIB .TXT UPLOAD VALIDATION ===")
    base_dir = Path("uploads").resolve()
    base_dir.mkdir(exist_ok=True)

    filename = input("Enter filename: ").strip()
    file_path = (base_dir / filename).resolve()

    if base_dir in file_path.parents or file_path == base_dir:
        if file_path.suffix.lower() == ".txt":
            print(f"\n[ACCESS ALLOWED]: {file_path}")
        else:
            print("\n[DENIED] Only .txt files are allowed.")
    else:
        print("\n[DENIED] Path traversal detected.")

if __name__ == "__main__":
    validate_txt_file()
