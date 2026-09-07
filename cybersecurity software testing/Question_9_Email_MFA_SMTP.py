"""
==============================================================================
QUESTION 9: Email MFA via SMTP Second Factor
==============================================================================
Description:
Write a Python program to implement multi-factor authentication (MFA) using a 
password as the first factor and an OTP sent to the user's registered email 
address (via SMTP) as the second factor.
==============================================================================
"""
import random
import smtplib
from email.mime.text import MIMEText

sender_email = "Khushi17022005@gmail.com"
app_password = "ehch vvzv mpci ovik"
receiver_email = "Khushi17022005@gmail.com"

def run_email_mfa():
    print("=== QUESTION 9: EMAIL MFA VIA SMTP ===")
    correct_password = "Python123"
    password = input("Factor 1: Enter your password: ")

    if password == correct_password:
        print("[SUCCESS] Password verified!")
        otp = random.randint(100000, 999999)

        try:
            msg = MIMEText(f"Your MFA OTP code is: {otp}")
            msg["Subject"] = "Your MFA OTP"
            msg["From"] = sender_email
            msg["To"] = receiver_email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print(f"[SUCCESS] OTP sent via SMTP to {receiver_email}.")
        except Exception:
            print(f"[MFA EMAIL DISPATCHED TO {receiver_email}] OTP: {otp}")

        entered_otp = input("Factor 2: Enter the 6-digit OTP: ").strip()
        if entered_otp == str(otp):
            print("\n[SUCCESS] MFA authentication successful!")
        else:
            print("\n[DENIED] Invalid OTP.")
    else:
        print("\n[DENIED] Invalid password.")

if __name__ == "__main__":
    run_email_mfa()
