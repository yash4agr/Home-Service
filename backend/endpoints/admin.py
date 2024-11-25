from flask import Blueprint, jsonify, request, send_file
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
import os

from database.models import (
    db, UserLogin, UserAddress, Professional, 
    ServiceRequest, ServiceStats, Services, Category
)

admin_router = Blueprint("admin", __name__)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = UserLogin.query.get(current_user_id)
        
            if not user or user.role != 'admin':
                return jsonify({"message": "Admin access required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@admin_router.route("/dashboard", endpoint="admin-dashboard")
@jwt_required()
@admin_required()
def dashboard():


    stats = ServiceStats.get_instance()
    return jsonify({"stats":{
        "total_users": stats.total_users,
        "total_professionals": stats.total_professionals,
        "totalRequests": stats.total_services,
        "total_completed_requests": stats.total_completed_requests,
        "activeServices": stats.total_pending_requests,
        "total_expired_requests": stats.total_expired_requests,
        "avg_rating": stats.avg_rating}
    })

# User-related routes
@admin_router.route("/users", endpoint="admin-get-users")
@jwt_required()
@admin_required()
def get_users():
    user_id = request.args.get('user_id')
    if user_id:
        user = UserLogin.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user.to_dict())
    users = UserLogin.query.all()
    return jsonify([user.to_dict() for user in users])
 

@admin_router.route("/users/<int:user_id>/ban-status", endpoint="ban-user", methods=['PATCH'])
@jwt_required()
@admin_required()
def ban_user(user_id):
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = UserLogin.query.get(user_id)
    if not user:
        return jsonify({ "message": f"No User found with id: { user_id }" }), 404
    
    try:
        user.is_banned = not user.is_banned
        db.session.commit()
        return jsonify({
            "message": f"User ban status updated to {user.is_banned}",
            "User": user.to_dict()
        }), 200
    except SQLAlchemyError as e:
        return jsonify({ "message": "An error occurred while banning the user", "error": str(e) }), 500


@admin_router.route("/users/<int:user_id>/address", endpoint="user-address")
@jwt_required()
@admin_required()
def user_address(user_id):
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = UserAddress.query.filter_by(user_login_id = user_id).first()
    if not user:
        return jsonify({ "message": f"No User found with id: { user_id }" }), 404
    
    return jsonify(user.to_dict())
    


@admin_router.route("/professionals/<int:user_id>/details", endpoint="professionals_details")
@jwt_required()
@admin_required()
def professionals_details(user_id):
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = Professional.query.filter_by(user_login_id = user_id).first()
    if not user:
        return jsonify({ "message": f"No Professinal found with id: { user_id }" }), 404
    
    return jsonify(user.to_dict())

@admin_router.route("/professionals/<int:user_id>/resume", endpoint="get_professional_resume")
@jwt_required()
@admin_required()
def get_professional_resume(user_id):
    professional = Professional.query.filter_by(id=user_id).first()
    if not professional or not professional.resume_path:
        return jsonify({"message": "Resume not found"}), 404
    
    try:
        return send_file(
            professional.resume_path,
            as_attachment=True,
            download_name=f"resume_{user_id}.pdf"
        )
    except Exception as e:
        return jsonify({"message": "Error retrieving resume", "error": str(e)}), 500


@admin_router.route("/professionals/<int:user_id>/reviews", endpoint="professionals_reviews")
@jwt_required()
@admin_required()
def professionals_reviews(user_id):
    professional = Professional.query.filter_by(user_login_id=user_id).first()
    if not professional:
        return jsonify({"message": f"No Professional found with id: {user_id}"}), 404
    
    service_requests = ServiceRequest.query.filter_by(professional_id=professional.id).all()
    return jsonify([{
        **request.to_dict(),
        "service_name": request.service.name,
        "customer_name": request.customer.name
    } for request in service_requests])

@admin_router.route("/exportMonthlyReport", endpoint="export_monthly_report")
@jwt_required()
@admin_required()
def exportMonthlyReport():
    
    ## DEFINE SENT LOGIC

    return jsonify({"message": "Monthly report scheduled"}), 200


# Professional verification routes
@admin_router.route("/professionals-pending", endpoint="professionals-pending")
@jwt_required()
@admin_required()
def pending_verification():
    professionals = db.session.query(UserLogin).join(UserLogin.professionals).filter(
        UserLogin.role == 'professional',
        Professional.is_approved == False
    ).all()

    if professionals:
        return jsonify([professional.to_dict() for professional in professionals]), 200
    return jsonify({"message": "No professional found"}), 200



@admin_router.route("/verify", endpoint="professional-verification", methods=['PUT'])
@jwt_required()
@admin_required()
def verification():
    user_id = request.args.get('user_id')
    approved = request.args.get('approved')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    professional = Professional.query.get(user_id)
    if not professional:
        return jsonify({ "message": f"No professional found with id: { user_id }" }), 404
    

    if professional.is_approved:
        return jsonify({ "message": f"Professional with id: { user_id } is already approved" }), 400
    
    try:
        professional.is_approved = True if approved=="true" else False
        db.session.commit()
        return jsonify({
            "message": f"Professional with id: {user_id} has been successfully approved",
            "professional": professional.to_dict()
        }), 200
    
    except SQLAlchemyError as e:
        return jsonify({ "message": "An error occurred while approving the professional", "error": str(e) }), 500



