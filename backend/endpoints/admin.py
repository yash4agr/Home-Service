from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from database.models import db, UserLogin, UserAddress, Professional, Services

admin_router = Blueprint("admin", __name__)


@admin_router.route("/dasboard", endpoint="admin-dashboard")
def dasboard():
    pass

@admin_router.route("/users", endpoint="admin-get-users")
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('q', '')

    # Start with the base query
    query = UserLogin.query

    if search_query:
        query = query.filter(
            or_(
                UserLogin.name.ilike(f'%{search_query}%'),
                UserLogin.email.ilike(f'%{search_query}%')
            )
        )

    # Limited to 100
    per_page = min(per_page, 100)

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

    user_address = UserAddress.query.get(user_login_id = user_id)
    
    if user.role=="Professional":
        professional = Professional.query.get(user_login_id = user_id)
        return jsonify({
            "message": f"Professional Details",
            "User": user.to_dict(),
            "Address": user_address.to_dict(),
            "professional": professional.to_dict()
        }), 200
    return jsonify({
            "message": f"Professional Details",
            "User": user.to_dict(),
            "Address": user_address.to_dict()
        }), 200
    

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


@admin_router.route("/services", methods=['GET'], endpoint="get-services")
def get_services():
    services = Services.query.all()
    return jsonify([service.to_dict() for service in services])


@admin_router.route("/services", methods=['POST'], endpoint="Create-service")
def create_services():
    form = NewService()
    if form.validate():
        new_service = Services(
            name=form.name.data,
            description=form.description.data,
            base_price=form.base_price.data,
            img=form.img.data,
            time_required=form.time_required.data,
            available=form.available.data,
        )
        try:
                # Add address to database
                db.session.add(new_service)
                db.session.commit()
                return jsonify({"message": "Address added successfully"}), 201
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({ "message": "An error occurred while adding the service", "error": str(e) }), 500
    return jsonify({ "message": "Invalid form data" }), 400

@admin_router.route("/services", methods=['PUT'], endpoint="Update-service")
def update_services():
    service_id = request.json.get('service_id')

    if not service_id:
        return jsonify({"message": "Service ID is required"}), 400

    service = Services.query.get(service_id)

    if not service:
        return jsonify({ "message": f"No service found with id: { service_id }" }), 404

    form = UpdateService()
    if form.validate():
        service.name = (form.name.data, service.name),
        service.description = (form.description.data, service.description),
        service.base_price = (form.base_price.data, service.base_price),
        service.img = (form.img.data, service.img),
        service.time_required = (form.time_required.data, service.time_required),
        service.available = (form.available.data, service.available),

        try:
            # Commit changes to database
            db.session.commit()
            return jsonify({"message": "Service updated successfully"}), 200
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({ "message": "An error occurred while updating the service", "error": str(e) }), 500
        
    return jsonify({ "message": "Invalid form data" }), 400

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


@admin_router.route("/verification", endpoint="professional-verification")
def verification():
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    user = Professional.query.get(user_id)

    if not user:
        return jsonify({ "message": f"No professional found with id: { user_id }" }), 404
    

    if user.is_approved:
        return jsonify({ "message": f"Professional with id: { user_id } is already approved" }), 400
    
    try:
        user.is_approved = True
        db.session.commit()
        return jsonify({
            "message": f"Professional with id: {user_id} has been successfully approved",
            "professional": user.to_dict()
        }), 200
    
    except SQLAlchemyError as e:
        return jsonify({ "message": "An error occurred while approving the professional", "error": str(e) }), 500



