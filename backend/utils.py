import redis
import random
import string
import smtplib
import  os
import uuid
from werkzeug.utils import secure_filename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Redis setup
redis_client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=int(os.environ.get('REDIS_PORT', 6379)), db=1, decode_responses=True)

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

def handle_image_upload(image_file, service_id=None):
    if not image_file:
        return None
        
    try:
        upload_dir = os.path.join('static', 'uploads', 'services')
        file_ext = os.path.splitext(secure_filename(image_file.filename))[1].lower()
        os.makedirs(upload_dir, exist_ok=True)
        if service_id:
            filename = f"service_{service_id}{file_ext}"
        else:
            filename = f"service_{uuid.uuid4().hex[:8]}{file_ext}"
        file_path = os.path.join(upload_dir, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)

        image_file.seek(0)
        image_file.save(file_path)
        path = os.path.relpath(file_path, start='static').replace(os.path.sep,'/')
        return file_path
        
    except Exception as e:
        print(f"Error handling image: {e}")
        return None

def handle_image_delete(file_path):
    if not file_path:
        return
       
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting image: {e}")

