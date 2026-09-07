"""
==============================================================================
QUESTION 27: Secure File Copying using Shutil & Pathlib
==============================================================================
Description:
Write a Python program to securely copy a file to a destination filename 
inside a designated uploads directory, but only after verifying that the 
resolved destination path lies within that directory, in order to prevent path 
traversal attacks.
==============================================================================
"""
from pathlib import Path
import shutil

def secure_copy():
    print("=== QUESTION 27: SECURE FILE COPYING ===")
    base_dir = Path("uploads").resolve()
    base_dir.mkdir(exist_ok=True)
    source = base_dir / "sample.txt"
    source.write_text("Sample file content.")

    filename = input("Enter destination filename: ").strip()
    dest = (base_dir / filename).resolve()

    if base_dir in dest.parents:
        shutil.copy(source, dest)
        print(f"\n[SUCCESS] Copied to: {dest}")
    else:
        print("\n[DENIED] Access denied!")

if __name__ == "__main__":
    secure_copy()
