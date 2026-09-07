"""
==============================================================================
QUESTION 15: Network Diagnostic Tool (Allowlisted Operations)
==============================================================================
Description:
Write a Python program to implement a network diagnostic tool that allows 
the user to select from a predefined (allowlisted) set of operations, such as 
pinging Google DNS or displaying the IP configuration, to prevent command 
injection attacks.
==============================================================================
"""
import subprocess
import os

def run_diagnostic():
    print("=== QUESTION 15: NETWORK DIAGNOSTIC TOOL ===")
    ping_flag = "-n" if os.name == 'nt' else "-c"
    ip_cmd = ["ipconfig"] if os.name == 'nt' else ["ifconfig"]
    allowed = {"1": ["ping", ping_flag, "2", "8.8.8.8"], "2": ip_cmd}

    print("1. Ping Google DNS (8.8.8.8)\n2. Display IP Configuration")
    choice = input("Select choice (1/2): ").strip()

    if choice in allowed:
        res = subprocess.run(allowed[choice], capture_output=True, text=True)
        print(res.stdout[:400] + "\n... [truncated]")
    else:
        print("\n[DENIED] Unauthorized operation.")

if __name__ == "__main__":
    run_diagnostic()
