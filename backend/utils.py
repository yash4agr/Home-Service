import redis
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Redis setup
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

def generate_otp(length=6):
    """Generate a random OTP."""
    return ''.join(random.choices(string.digits, k=length))

def store_otp(email, otp, verification_type):
    """Store OTP in Redis with expiration."""
    redis_key = f"otp:{verification_type}:{email}"
    redis_client.setex(redis_key, 600, otp)

def get_stored_otp(email, verification_type):
    """Retrieve stored OTP from Redis."""
    redis_key = f"otp:{verification_type}:{email}"
    return redis_client.get(redis_key)

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "donotreply@homeservice.com"
SENDER_PASSWORD = "password"

def send_otp_email(to, otp):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to
    msg['Subject'] = 'Your Verification Code'

    msg.attach(MIMEText(f'Your verification code is: {otp}', 'html'))

    smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    smtp_server.send_message(msg)
    smtp_server.quit()

