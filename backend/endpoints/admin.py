from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from database.models import db, UserLogin, Professional

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



