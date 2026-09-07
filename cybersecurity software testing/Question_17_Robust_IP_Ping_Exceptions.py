"""
==============================================================================
QUESTION 17: IP Ping with Exception Handling
==============================================================================
Description:
Write a Python program to validate a user-entered IP address and safely execute 
a ping command using subprocess, handling invalid IP addresses and ping 
failures using exception handling.
==============================================================================
"""
import subprocess
import ipaddress
import os

def ping_with_exceptions():
    print("=== QUESTION 17: ROBUST IP PING WITH EXCEPTION HANDLING ===")
    address = input("Enter IP address: ").strip()

    try:
        ipaddress.ip_address(address)
        flag = "-n" if os.name == 'nt' else "-c"
        subprocess.run(["ping", flag, "2", address], check=True, capture_output=True)
        print("\n[SUCCESS] Ping operation succeeded!")
    except ValueError:
        print("\n[ERROR] Invalid IP address format.")
    except subprocess.CalledProcessError:
        print("\n[ERROR] Ping operation failed (Unreachable host).")

if __name__ == "__main__":
    ping_with_exceptions()
