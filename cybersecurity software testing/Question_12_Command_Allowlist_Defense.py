"""
==============================================================================
QUESTION 12: Command Injection Defense via Allowlisting
==============================================================================
Description:
Write a Python program to allow a user to execute only a predefined 
(allowlisted) set of system commands — date, whoami, pwd, and list — 
in order to prevent command injection attacks.
==============================================================================
"""
import subprocess
import os

def run_allowlist_command():
    print("=== QUESTION 12: COMMAND ALLOWLISTING DEFENSE ===")
    allowed_commands = {
        "date": ["powershell", "-Command", "Get-Date"] if os.name == 'nt' else ["date"],
        "whoami": ["whoami"],
        "pwd": ["powershell", "-Command", "Get-Location"] if os.name == 'nt' else ["pwd"],
        "list": ["dir"] if os.name == 'nt' else ["ls"]
    }

    print("Allowed commands: date | whoami | pwd | list")
    command = input("Enter command: ").lower().strip()

    if command in allowed_commands:
        print(f"\n[EXECUTING]: {command}\n")
        res = subprocess.run(allowed_commands[command], capture_output=True, text=True, shell=(os.name=='nt' and command=='list'))
        print(res.stdout)
    else:
        print("\n[DENIED] Unauthorized command execution attempt blocked.")

if __name__ == "__main__":
    run_allowlist_command()
