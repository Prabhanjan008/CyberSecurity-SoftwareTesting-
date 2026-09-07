"""
==============================================================================
QUESTION 31: Comprehensive Secure File Upload System
==============================================================================
Description:
Write a Python program to implement a secure file upload system that rejects 
empty filenames, path traversal attempts, and absolute paths; restricts uploads 
to allowed file extensions (PDF, JPG, JPEG, PNG); sanitizes the filename; 
generates a unique filename; and enforces a maximum file size limit of 5 MB.
==============================================================================
"""
import os
import re
import uuid

def process_upload():
    print("=== QUESTION 31: COMPREHENSIVE SECURE FILE UPLOAD SYSTEM ===")
    upload_folder = "uploads"
    max_size = 5 * 1024 * 1024
    allowed_exts = {".pdf", ".jpg", ".jpeg", ".png", ".txt"}

    os.makedirs(upload_folder, exist_ok=True)
    sample = "test_sample.png"
    if not os.path.exists(sample):
        with open(sample, "wb") as f:
            f.write(b"PNG_SAMPLE_BYTES")

    filename = input("Enter filename to upload (e.g. test_sample.png): ").strip()

    try:
        if not filename:
            print("\n[ERROR] Filename cannot be empty.")
        elif ".." in filename or "/" in filename or "\\" in filename:
            print("\n[ERROR] Path traversal attempt detected!")
        elif os.path.isabs(filename):
            print("\n[ERROR] Absolute paths are not allowed.")
        else:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in allowed_exts:
                print(f"\n[ERROR] Invalid file type. Allowed: {allowed_exts}")
            else:
                orig_name = os.path.splitext(os.path.basename(filename))[0]
                safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", orig_name) or "uploaded_file"
                unique_name = f"{safe_name}_{str(uuid.uuid4())[:8]}{ext}"
                dest = os.path.join(upload_folder, unique_name)

                if not os.path.exists(filename):
                    print("\n[ERROR] Source file does not exist.")
                elif os.path.getsize(filename) > max_size:
                    print("\n[ERROR] File size exceeds 5 MB limit.")
                else:
                    with open(filename, "rb") as src, open(dest, "wb") as tgt:
                        tgt.write(src.read())
                    print(f"\n[SUCCESS] File uploaded successfully!")
                    print("Saved Unique Name:", unique_name)
    except Exception:
        print("\n[ERROR] Unable to process file safely.")

if __name__ == "__main__":
    process_upload()
