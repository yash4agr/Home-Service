from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone

from database.models import db, UserLogin, UserAddress, Professional, Services
# from forms import ProfessionalSignupForm

professional_router = Blueprint("professional", __name__)

# Configure file upload
UPLOAD_FOLDER = 'uploads/resumes'
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
        service_category = form_data.get('serviceCategory')
        service = Services.query.filter_by(name=service_category).first()
        # if not service:
        #     return jsonify({"message": "Invalid service category"}), 400

        # Create professional profile
        professional = Professional(
            user_login_id=user_id,
            service_id=service.id,
            experience=form_data.get('yearsOfExperience'),
            resume_path=resume_path,
            is_approved=False
        )

        # Update user's phone number if provided
        phone_number = form_data.get('phoneNumber')
        if phone_number:
            user.phone_number = phone_number
            user.name = form_data.get('fullName', user.name)

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
                    "service": service.name,
                    "experience": professional.experience,
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
            "is_approved": professional.is_approved,
            "service": professional.service.name,
            "created_at": professional.created_at
        })
        
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500