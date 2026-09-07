"""
==============================================================================
QUESTION 18: Logged System Operations (Logging Module Integration)
==============================================================================
Description:
Write a Python program to execute a predefined (allowlisted) set of system 
operations selected by the user (display current user, current directory, date 
and time, or list files) and log each selected operation and its execution 
status to a log file.
==============================================================================
"""
import subprocess
import logging
import os

logging.basicConfig(filename="operation_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def run_logged_ops():
    print("=== QUESTION 18: LOGGED SYSTEM OPERATIONS ===")
    ops = {
        "1": {"name": "Display current user", "cmd": ["whoami"]},
        "2": {"name": "Display current directory", "cmd": ["powershell", "-Command", "Get-Location"] if os.name=='nt' else ["pwd"]},
        "3": {"name": "Display current date", "cmd": ["powershell", "-Command", "Get-Date"] if os.name=='nt' else ["date"]},
        "4": {"name": "List files", "cmd": ["dir"] if os.name=='nt' else ["ls"]}
    }

    print("1. Current User | 2. Directory | 3. Date & Time | 4. List Files")
    choice = input("Select operation (1-4): ").strip()

    if choice in ops:
        op = ops[choice]
        logging.info(f"Selected: {op['name']}")
        res = subprocess.run(op["cmd"], capture_output=True, text=True, shell=(os.name=='nt' and choice=='4'))
        print(res.stdout)
        logging.info(f"Executed successfully: {op['name']}")
        print("[LOGGED] Event written to 'operation_log.txt'.")
    else:
        print("\n[DENIED] Unauthorized choice.")
        logging.warning(f"Unauthorized attempt: {choice}")

if __name__ == "__main__":
    run_logged_ops()
