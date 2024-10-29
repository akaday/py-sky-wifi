import re
import random
import string
import time
from typing import Dict

# In-memory storage for OTPs and failed login attempts
otp_storage: Dict[str, Dict[str, str]] = {}
failed_login_attempts: Dict[str, int] = {}
locked_accounts: Dict[str, float] = {}

def enforce_password_policy(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def generate_otp(username: str) -> str:
    otp = ''.join(random.choices(string.digits, k=6))
    otp_storage[username] = {"otp": otp, "timestamp": time.time()}
    return otp

def verify_otp(username: str, otp: str) -> bool:
    if username not in otp_storage:
        return False
    stored_otp = otp_storage[username]["otp"]
    timestamp = otp_storage[username]["timestamp"]
    if time.time() - timestamp > 300:  # OTP expires after 5 minutes
        del otp_storage[username]
        return False
    if otp == stored_otp:
        del otp_storage[username]
        return True
    return False

def track_failed_login_attempts(username: str):
    if username not in failed_login_attempts:
        failed_login_attempts[username] = 0
    failed_login_attempts[username] += 1
    if failed_login_attempts[username] >= 5:
        lock_account(username)

def lock_account(username: str):
    locked_accounts[username] = time.time()

def unlock_account(username: str):
    if username in locked_accounts:
        del locked_accounts[username]
    if username in failed_login_attempts:
        del failed_login_attempts[username]

def is_account_locked(username: str) -> bool:
    if username not in locked_accounts:
        return False
    lock_time = locked_accounts[username]
    if time.time() - lock_time > 900:  # Account lock expires after 15 minutes
        unlock_account(username)
        return False
    return True
