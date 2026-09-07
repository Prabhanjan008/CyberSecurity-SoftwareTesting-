"""
==============================================================================
QUESTION 20: Path Traversal Prevention (Uploads Boundary Check)
==============================================================================
Description:
Write a Python program to accept a filename from the user and verify that the 
resulting file path remains within a designated uploads directory, in order to 
detect and prevent path traversal attacks.
==============================================================================
"""
import os

def check_path_traversal():
    print("=== QUESTION 20: PATH TRAVERSAL PREVENTION ===")
    uploads_dir = os.path.abspath("uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    filename = input("Enter filename: ").strip()
    file_path = os.path.abspath(os.path.join(uploads_dir, filename))

    if file_path.startswith(uploads_dir + os.sep) or file_path == uploads_dir:
        print(f"\n[SAFE] Path remains inside uploads directory:\n{file_path}")
    else:
        print(f"\n[ALERT] Path traversal detected! Access denied.")

if __name__ == "__main__":
    check_path_traversal()
