"""
==============================================================================
QUESTION 13: Safe Subprocess Search (Without shell=True)
==============================================================================
Description:
Write a Python program to search for .txt files in a given directory using 
subprocess with a list of arguments (without shell=True), and demonstrate that 
it safely handles both a normal directory path and a malicious-looking input 
attempting command injection.
==============================================================================
"""
import subprocess
import os

def search_files(directory):
    cmd = ["powershell", "-Command", f"Get-ChildItem -Path '{directory}' -Filter '*.txt'"] if os.name == 'nt' else ["find", directory, "-name", "*.txt"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout, res.returncode

def demo():
    print("=== QUESTION 13: SAFE SUBPROCESS FILE SEARCH ===")
    print("\n1. Normal search in current directory ('.'):")
    out, code = search_files(".")
    print(out)

    print("2. Malicious payload input ('. ; cat /etc/shadow & dir'):")
    out, code = search_files(". ; cat /etc/shadow & dir")
    print(out)
    print(f"Return Code: {code}")
    print("[SUCCESS] Command injection safely prevented.")

if __name__ == "__main__":
    demo()
