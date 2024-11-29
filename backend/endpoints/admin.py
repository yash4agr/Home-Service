from flask import Blueprint, jsonify, request, send_file
from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone
from functools import wraps
import os

from database.models import (
    db, UserLogin, UserAddress, Professional, 
    ServiceRequest, ServiceStats
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

    service_stats = ServiceStats.get_instance()
    
    # stats
    stats = {
        'totalRequests': ServiceRequest.query.count(),
        'activeServices': ServiceRequest.query.filter_by(
                            status='accepted'
                        ).count(),
        'completionRate': calculate_completion_rate(),
        'avg_rating': service_stats.avg_rating,
    }
    
    # Calculate past 7 days service requests and revenue
    service_data = get_past_seven_days_admin_data()
    return jsonify({
        'stats': stats,
        'serviceData': service_data['service_requests'],
        'revenueData': service_data['revenue'],
        'days': service_data['days']
    })

def calculate_completion_rate():
    total_requests = ServiceRequest.query.count()
    completed_requests = ServiceRequest.query.filter_by(
        status='completed'
    ).count()

    if total_requests == 0:
        return 0
    
    return round((completed_requests / total_requests) * 100, 2)

def get_past_seven_days_admin_data():
    current_time = datetime.now(timezone.utc)
    seven_days_ago = current_time - timedelta(days=7)
    
    daily_requests = db.session.query(
        func.date(ServiceRequest.created_at).label('day'),
        func.count(ServiceRequest.id).label('request_count')
    ).filter(
        ServiceRequest.created_at >= seven_days_ago
    ).group_by('day').order_by('day').all()
    
    daily_revenue = db.session.query(
        func.date(ServiceRequest.created_at).label('day'),
        func.sum(ServiceRequest.total_amount).label('total_revenue')
    ).filter(
        and_(
            ServiceRequest.created_at>= seven_days_ago,
            ServiceRequest.status == 'completed',
            ServiceRequest.total_amount.isnot(None)
        )
    ).group_by('day').order_by('day').all()

    days = [(current_time - timedelta(days=x)).date() for x in range(6, -1, -1)]
    service_requests = [0] * 7
    revenue = [0.0] * 7
    
    for day, count in daily_requests:
        day_date = datetime.strptime(day, '%Y-%m-%d').date()
        if day_date in days:
            service_requests[days.index(day_date)] = count
    
    for day, daily_total in daily_revenue:
        day_date = datetime.strptime(day, '%Y-%m-%d').date()
        if day_date in days:
            revenue[days.index(day_date)] = round(daily_total or 0, 2)
    
    return {
        'service_requests': service_requests,
        'revenue': revenue,
        'days': [day.strftime('%Y-%m-%d') for day in days]
    }

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
    detail = user.to_dict()
    total_requests = ServiceRequest.query.filter_by(professional_id=user.id).count()
    pending_requests = ServiceRequest.query.filter_by(
        professional_id=user.id, 
        status='accepted'
    ).count()
    detail["total_requests"] = total_requests
    detail["pending_requests"] = pending_requests
    return jsonify(detail)

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
        "review": request.review,
        "service_name": request.service.name,
        "customer_name": request.customer.name
    } for request in service_requests])

@admin_router.route("/exportServiceRequest", endpoint="export_service_request")
@jwt_required()
@admin_required()
def exportServiceRequest():
    from celery_task import export_service_requests_to_csv
    user = UserLogin.query.get(get_jwt_identity())
    export_service_requests_to_csv.delay(user.email)

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
    return jsonify({"message": "No professional found"}), 404



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



