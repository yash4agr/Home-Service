import csv
import os
from datetime import datetime, timedelta, timezone

from flask import current_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import base64

from database.models import db, ServiceRequest, Professional, UserLogin, UserAddress, ServiceStats
from utils import (
    SMTP_SERVER_HOST, 
    SMTP_SERVER_PORT, 
    SENDER_ADDRESS, 
    SENDER_PASSWORD,
    redis_client
)

from app import celery


@celery.task
def send_daily_professional_reminders():
    # Find professionals with pending service requests
    pending_requests = ServiceRequest.query.filter_by(status='accepted').all()
    
    for request in pending_requests:
        # Check if professional exists and has pending requests
        if request.professional and request.professional.user_login:
            professional = request.professional
            professional_email = professional.user_login.email
            
            # Compose email
            msg = MIMEMultipart()
            msg['From'] = SENDER_ADDRESS
            msg['To'] = professional_email
            msg['Subject'] = 'Pending Service Request Reminder'
            
            # Email body
            body = f"""
            Dear {professional.user_login.name},
            
            You have a pending service request that requires your attention:
            
            Service: {request.service.name}
            Request Date: {request.date_of_request}
            Status: Pending
            
            Please complete the service on time.
            
            Best regards,
            Home Service Team
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            try:
                smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
                smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
                smtp_server.send_message(msg)
                smtp_server.quit()
            except Exception as e:
                print(f"Failed to send reminder email: {e}")

@celery.task()
def send_monthly_activity_report():
    # Get stats for the previous month
    stats = ServiceStats.get_instance()
    
    # Find all users
    users = UserLogin.query.filter_by(role='user').all()
    
    for user in users:
        # Compose email
        msg = MIMEMultipart()
        msg['From'] = SENDER_ADDRESS
        msg['To'] = user.email
        msg['Subject'] = 'Monthly Service Activity Report'
        
        # HTML report template
        html_report = f"""
        <html>
        <body>
            <h1>Monthly Service Activity Report</h1>
            <p>Dear {user.name},</p>
            
            <h2>Service Statistics</h2>
            <ul>
                <li>Total Services: {stats.total_services}</li>
                <li>Completed Requests: {stats.total_completed_requests}</li>
                <li>Pending Requests: {stats.total_pending_requests}</li>
                <li>Average Service Rating: {stats.avg_rating:.2f}</li>
            </ul>
            
            <p>Thank you for using our service!</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_report, 'html'))
        
        # Send email
        try:
            smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
            smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
            smtp_server.send_message(msg)
            smtp_server.quit()
        except Exception as e:
            print(f"Failed to send monthly report: {e}")

@celery.task
def export_service_requests_to_csv(admin_email):
    # Get completed service requests
    completed_requests = ServiceRequest.query.filter_by(status='completed').all()
    
    # Generate unique filename
    filename = f'service_requests_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    filepath = os.path.join(current_app.config.get('EXPORT_FOLDER', '/tmp'), filename)
    print(filepath)
    
    # Create CSV
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = [
            'service_id', 'customer_id', 'professional_id', 
            'date_of_request', 'date_of_completion', 
            'status', 'rating', 'review', 'total_amount'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for request in completed_requests:
            writer.writerow({
                'service_id': request.service_id,
                'customer_id': request.customer_id,
                'professional_id': request.professional_id,
                'date_of_request': request.date_of_request,
                'date_of_completion': request.date_of_completion,
                'status': request.status,
                'rating': request.rating,
                'review': request.review,
                'total_amount': request.total_amount
            })
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = admin_email
    msg['Subject'] = 'Service Requests Export'
    
    # Attach CSV
    with open(filepath, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    
    msg.attach(attachment)
    
    try:
        smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
        smtp_server.send_message(msg)
        smtp_server.quit()

        os.remove(filepath)
    except Exception as e:
        print(f"Failed to export service requests: {e}")

@celery.task
def check_expired_service_requests():
    current_time = datetime.now(timezone.utc)
    twenty_four_hours_ago = current_time - timedelta(hours=24)
    
    pending_requests = ServiceRequest.query.filter(
        ServiceRequest.status == 'pending',
        ServiceRequest.date_of_request < twenty_four_hours_ago
    ).all()
    
    for request in pending_requests:
        # Check if any professionals are available in the area
        professionals_count = Professional.query.join(UserLogin) \
            .join(UserAddress) \
            .filter(
                Professional.category_id == request.service.category_id,
                Professional.is_approved == True,
                UserAddress.zip_code == request.address.zip_code
            ).count()
        
        # Get existing rejections
        key = f'service_request_rejections:{request.id}'
        rejected_count = redis_client.scard(key)
        
        if rejected_count >= professionals_count:
            request.status = 'rejected'
        else:
            request.status = 'expired'
    
    db.session.commit()