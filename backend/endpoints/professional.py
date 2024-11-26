from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone

from database.models import db, UserLogin, UserAddress, Professional, Category, ServiceRequest
from utils import redis_client

professional_router = Blueprint("professional", __name__)

# Configure file upload
UPLOAD_FOLDER = 'database/uploads/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_resume(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)
    return file_path

@professional_router.route("/signup", methods=["POST"])
@jwt_required()
def professional_signup():
    try:
        user_id = get_jwt_identity()
        user = UserLogin.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        if not user.is_email_verified:
            return jsonify({"message": "Please verify your email first"}), 403
            
        if Professional.query.filter_by(user_login_id=user_id).first():
            return jsonify({"message": "Professional profile already exists"}), 400

        # Get form data
        form_data = request.form.to_dict()
        
        # Validate and save the resume file
        if 'resume' not in request.files:
            return jsonify({"message": "Resume file is required"}), 400
            
        resume_file = request.files['resume']
        if not allowed_file(resume_file.filename):
            return jsonify({"message": "Invalid file type. Allowed types: PDF, DOC, DOCX"}), 400
            
        # Save the resume file
        resume_path = save_resume(resume_file)

        # Create address
        address = UserAddress(
            user_login_id=user_id,
            street=form_data.get('address.locality'),
            city=form_data.get('address.city'),
            state=form_data.get('address.state'),
            zip_code=form_data.get('address.pincode'),
            country=form_data.get('address.country', 'India'),
            address_type='professional'
        )
        
        # Get or create service
        category_id  = form_data.get('serviceCategory')
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Invalid service category"}), 400

        # Create professional profile
        professional = Professional(
            user_login_id=user_id,
            category_id=category.id,
            experience=form_data.get('yearsOfExperience'),
            resume_path=resume_path,
            is_approved=False
        )

        # Update user's phone number if provided
        phone_number = form_data.get('phoneNumber')
        if phone_number:
            user.phone_number = phone_number
        user.name = form_data.get('fullName', user.name)
        user.role = "professional"

        try:
            db.session.add(address)
            db.session.add(professional)
            db.session.commit()

            return jsonify({
                "message": "Professional profile created successfully",
                "data": {
                    "id": professional.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone_number,
                    "service": category.name,
                    "experience": professional.experience,
                    "rating": professional.avg_rating,
                    "total_services": professional.total_services,
                    "is_approved": professional.is_approved,
                    "address": {
                        "street": address.street,
                        "city": address.city,
                        "state": address.state,
                        "zip_code": address.zip_code,
                        "country": address.country
                    }
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            # Delete uploaded file if database operation fails
            if os.path.exists(resume_path):
                os.remove(resume_path)
            return jsonify({"message": "Database error occurred", "error": str(e)}), 500

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@professional_router.route("/status", methods=["GET"])
@jwt_required()
def check_status():
    try:
        user_id = get_jwt_identity()
        professional = Professional.query.filter_by(user_login_id=user_id).first()
        
        if not professional:
            return jsonify({"message": "Professional profile not found"}), 404
            
        return jsonify({
            "id": professional.id,
            "is_approved": professional.is_approved,
            "category": professional.category.name,
            "experience": professional.experience,
            "rating": professional.avg_rating,
            "total_services": professional.total_services,
            "created_at": professional.created_at.isoformat(),
            "updated_at": professional.updated_at.isoformat()
        })
        
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@professional_router.route('/service_actions', methods=['POST'])
@jwt_required()
def service_actions():
    current_user = UserLogin.query.get(get_jwt_identity())
    professional = Professional.query.filter_by(user_login_id=current_user.id).first()
    
    data = request.get_json()
    service_request_id = data.get('service_request_id')
    action = str(data.get('action')).strip()  # 'accept', 'reject', 'completed', 'canceled'
    
    service_request = ServiceRequest.query.get(service_request_id)
    
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404
    
    if action == 'accept':

        if not professional:
            return jsonify({'message': 'Not a registered professional'}), 403
        # Check if service request is still pending
        if service_request.status != 'pending':
            return jsonify({'message': 'Service request cannot be accepted'}), 400
        
        service_request.professional_id = professional.id
        service_request.status = 'accepted'
        
        # Clear any previous rejections in Redis
        redis_client.delete(f'service_request_rejections:{service_request_id}')
    
    elif action == 'reject':
        if not professional:
            return jsonify({'message': 'Not a registered professional'}), 403
        
        # Track rejections in Redis
        key = f'service_request_rejections:{service_request_id}'
        redis_client.sadd(key, professional.id)
        
        # Check total rejections
        total_professionals_in_area = Professional.query.join(UserLogin) \
            .join(UserAddress) \
            .filter(
                Professional.category_id == service_request.service.category_id,
                Professional.is_approved == True,
                UserAddress.zip_code == service_request.address.zip_code
            ).count()
        
        rejected_count = redis_client.scard(key)
        
        if rejected_count >= total_professionals_in_area:
            service_request.status = 'rejected'
    
    elif action == 'completed':
        # Validate completion
        if service_request.professional_id == professional.id or service_request.customer_id == get_jwt_identity():
            rating = data.get('rating')
            review = data.get('review')
            
            service_request.complete_service(rating=rating, review=review)
        else:
            return jsonify({'message': 'Not authorized to complete this service'}), 403
        
        
    
    elif action == "canceled":
        print("hry")
        if professional:
            if service_request.professional_id == professional.id:
                service_request.status = 'canceled by professional'
        elif service_request.customer_id == get_jwt_identity():
            print("hry")
            service_request.status = 'canceled by customer'
        else:
            return jsonify({'message': 'Not authorized to complete this service'}), 403
    
    db.session.commit()
    return jsonify({'message': f'Service request {action}d successfully'}), 200