from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from database.models import db, UserLogin, UserAddress, Professional, Services
from forms import ServiceForm

admin_router = Blueprint("admin", __name__)


@admin_router.route("/dasboard", endpoint="admin-dashboard")
def dasboard():
    pass

# User-related routes
@admin_router.route("/users", endpoint="admin-get-users")
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search_query = request.args.get('q', '')

    query = UserLogin.query
    if search_query:
        query = query.filter(
            or_(
                UserLogin.name.ilike(f'%{search_query}%'),
                UserLogin.email.ilike(f'%{search_query}%')
            )
        )

    # Apply pagination to the query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items

    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'search_query': search_query
    })


@admin_router.route("/user", endpoint="user-detail")
def get_user():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = UserLogin.query.get(user_id)
    if not user:
        return jsonify({ "message": f"No User found with id: { user_id }" }), 404

    user_address = UserAddress.query.filter_by(user_login_id = user_id).first()
    
    response = {
            "message": f"Professional Details",
            "User": user.to_dict(),
            "Address": user_address.to_dict() if user_address else None
        }
    
    if user.role == "Professional":
        professional = Professional.query.filter_by(user_login_id = user_id).first()
        if professional:
            response["professional"] = professional.to_dict()

    return jsonify(response), 200
    

@admin_router.route("/ban-user", endpoint="ban-user")
def ban_user():
    user_id = request.json.get('user_id')
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

# Service-related routes
@admin_router.route("/services", methods=['GET'], endpoint="get-services")
def get_services():
    service_id = request.args.get('service_id')
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search_query = request.args.get('q', '')

    if service_id:
        service = Services.query.get(service_id)
        if not service:
            return jsonify({"message": f"No service with id: { service_id }"}), 404
        return jsonify(service.to_dict())

    query = Services.query
    if search_query:
        query = query.filter(
            or_(
                Services.name.ilike(f'%{search_query}%'),
                Services.description.ilike(f'%{search_query}%')
            )
        )

    # Apply pagination to the query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    services = pagination.items

    return jsonify({
        'services': [service.to_dict() for service in services],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'search_query': search_query
    })


@admin_router.route("/services", methods=['POST'], endpoint="upsert-service")
def create_or_update_service():
    form = ServiceForm(request.form)
    if form.validate():
        try:
            service_id = request.args.get('service_id')
            if service_id:
                service = Services.query.get(service_id)
                if not service:
                    return jsonify({"message": f"No service found with id: { service_id }"}), 404
                form.populate_obj(service)
            else:
                service = Services()
                form.populate_obj(service)
                db.session.add(service)
            
            db.session.commit()
            return jsonify(service.to_dict()), 200 if service_id else 201
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({ "message": "An error occurred while saving the service", "error": str(e) }), 500
    return jsonify({"message": "Validation error", "errors": form.errors}), 422


@admin_router.route("/services", methods=['DELETE'], endpoint="Delete-service")
def delete_service():
    service_id = request.json.get('service_id')
    if not service_id:
        return jsonify({"message": "Service ID is required"}), 400

    service = Services.query.get(service_id)
    if not service:
        return jsonify({ "message": f"No Service found with id: { service_id }" }), 404
    
    try:
        # Delete service from database
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted successfully"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({ "message": "An error occurred while deleting the service", "error": str(e) }), 500
    

# Professional verification routes
@admin_router.route("/pending-verification", endpoint="pending-verification")
def pending_verification():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search_query = request.args.get('q', '')

    # Start with the base query
    query = Professional.query.filter(Professional.is_approved == False)
    if search_query:
        query = query.filter(
            or_(
                Professional.name.ilike(f'%{search_query}%'),
                Professional.email.ilike(f'%{search_query}%')
            )
        )

    # Apply pagination to the query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    professionals = pagination.items

    return jsonify({
        'professionals': [professional.to_dict() for professional in professionals],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'search_query': search_query
    })



@admin_router.route("/verification", endpoint="professional-verification")
def verification():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    professional = Professional.query.get(user_id)
    if not professional:
        return jsonify({ "message": f"No professional found with id: { user_id }" }), 404
    

    if professional.is_approved:
        return jsonify({ "message": f"Professional with id: { user_id } is already approved" }), 400
    
    try:
        professional.is_approved = True
        db.session.commit()
        return jsonify({
            "message": f"Professional with id: {user_id} has been successfully approved",
            "professional": professional.to_dict()
        }), 200
    
    except SQLAlchemyError as e:
        return jsonify({ "message": "An error occurred while approving the professional", "error": str(e) }), 500



