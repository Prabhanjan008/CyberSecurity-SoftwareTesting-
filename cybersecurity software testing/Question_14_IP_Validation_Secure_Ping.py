"""
==============================================================================
QUESTION 14: IP Address Validation & Secure Ping
==============================================================================
Description:
Write a Python program to validate a user-entered IP address and then securely 
ping it using subprocess (without shell=True), to prevent command injection attacks.
==============================================================================
"""
import ipaddress
import subprocess
import os

def ping_ip():
    print("=== QUESTION 14: IP VALIDATION & SECURE PING ===")
    ip_str = input("Enter IP address to ping: ").strip()

    try:
        ipaddress.ip_address(ip_str)
        print(f"\n[VALIDATED] IP '{ip_str}' is valid. Pinging...")
        flag = "-n" if os.name == 'nt' else "-c"
        res = subprocess.run(["ping", flag, "2", ip_str], capture_output=True, text=True)
        print(res.stdout)
    except ValueError:
        print("\n[ERROR] Invalid IP address format entered!")

if __name__ == "__main__":
    ping_ip()
