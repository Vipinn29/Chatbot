import pyotp
from email_validator import validate_email
import smtplib
from email.message import EmailMessage

# Dummy storage for OTPs
otp_storage = {}

def generate_otp(email):
    """
    Generates a time-based one-time password (TOTP) for the given email.
    
    Args:
        email (str): The email address to generate the OTP for.
    
    Returns:
        str: The generated OTP.
    """
    try:
        validate_email(email)
    except Exception as e:
        raise ValueError("Invalid email address")
    
    # Create a new TOTP instance for the user
    totp = pyotp.TOTP('base32secret3232')
    otp = totp.now()
    otp_storage[email] = otp
    
    # Send OTP via email
    msg = EmailMessage()
    msg.set_content(f"Your one-time password (OTP) is: {otp}")
    msg['Subject'] = "Your One-Time Password (OTP)"
    msg['From'] = "your_email@example.com"
    msg['To'] = email
    
    server = smtplib.SMTP_SSL("smtp.elasticemail.com", 2525)
    server.login("bytebazaar22@gmail.com", "3EE497C9F6A898B7DD6714E88281E44FB91F")
    server.send_message(msg)
    server.quit()
    
    return otp
def verify_2fa(email, otp):
    correct_otp = otp_storage.get(email)
    return correct_otp == otp
