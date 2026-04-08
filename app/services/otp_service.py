import random
import time

otp_store = {}

def generate_otp():
    return str(random.randint(1000, 9999))

def save_otp(email: str, otp: str, expiry_seconds: int = 120):
    otp_store[email] = {
        "otp": otp,
        "expiry": time.time() + expiry_seconds,
        "is_used": False
    }

def verify_otp(email: str, user_otp: str):
    record = otp_store.get(email)

    if not record:
        return "Email not found. Please enter your registered email address."

    elif record["is_used"]:
        return "OTP already used"
    
    elif time.time() > record["expiry"]:
        return "OTP expired"

    elif record["otp"] != user_otp:
        return "Invalid OTP"

    record["is_used"] = True
    return "OTP verified successfully"
    