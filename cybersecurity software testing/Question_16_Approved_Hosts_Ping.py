"""
==============================================================================
QUESTION 16: Approved Hosts Ping Tool
==============================================================================
Description:
Write a Python program to allow the user to ping only a predefined list of 
approved hosts, in order to prevent command injection attacks.
==============================================================================
"""
import subprocess
import os

def ping_approved():
    print("=== QUESTION 16: APPROVED HOSTS PING TOOL ===")
    approved = {"1": "localhost", "2": "127.0.0.1"}
    print("1. localhost\n2. 127.0.0.1")
    choice = input("Select host choice (1/2): ").strip()

    if choice in approved:
        host = approved[choice]
        print(f"\n[PINGING]: {host}")
        flag = "-n" if os.name == 'nt' else "-c"
        subprocess.run(["ping", flag, "2", host])
    else:
        print("\n[DENIED] Host choice not in approved allowlist.")

if __name__ == "__main__":
    ping_approved()
