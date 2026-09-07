"""
==============================================================================
QUESTION 8: Mobile SMS OTP Verification System
==============================================================================
Description:
Write a Python program to implement a mobile-based OTP verification system 
that generates a random 6-digit OTP, validates the mobile number format, 
sends the OTP via SMS, and verifies the OTP entered by the user within a 
2-minute expiry window.
==============================================================================
"""
import random
import time
import re

def validate_mobile_number(phone):
    return bool(re.match(r'^\+?[1-9]\d{1,14}$', phone))

def run_mobile_otp():
    print("=== QUESTION 8: MOBILE SMS OTP VERIFICATION SYSTEM ===")
    mobile_number = input("Enter mobile number (e.g. +919480095248): ").strip()

    if not validate_mobile_number(mobile_number):
        print("\n[ERROR] Invalid mobile number format.")
        return

    otp_code = str(random.randint(100000, 999999))
    expiry_duration = 120
    sent_time = time.time()

    print("="*60)
    print("             [SIMULATED SMS SANDBOX]")
    print(f" To   : {mobile_number}")
    print(f" Body : Your OTP code is {otp_code}. Valid for 2 minutes.")
    print("="*60)

    user_otp = input("\nEnter the 6-digit OTP received: ").strip()
    elapsed = time.time() - sent_time

    if elapsed > expiry_duration:
        print("\n[EXPIRED] OTP has expired.")
    elif user_otp == otp_code:
        print("\n[SUCCESS] Mobile OTP verified! Access granted.")
    else:
        print("\n[DENIED] Invalid OTP entered.")

if __name__ == "__main__":
    run_mobile_otp()
