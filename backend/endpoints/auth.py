from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token , jwt_required, get_jwt_identity, get_jwt

from database.models import db, User
from forms import RegistrationForm, LoginForm

auth_router = Blueprint("auth", __name__)


# Routes
@auth_router.route("/register", methods=["POST"], endpoint="auth-register")
def register():
    form = RegistrationForm()
    if form.validate():
        email = form.email.data
        password = form.password.data
    
        if User().validate_email(email):
            return jsonify({ "message": "User with this email already exists" }), 400
        
        new_user = User(email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(identity = new_user.id)
            refresh_token = create_refresh_token(identity = new_user.id)
            return jsonify({
                "message": "User registered successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500
    return jsonify({ "message": "Validation failed", }), 500

@auth_router.route("/login", methods=["POST"], endpoint="auth-login")
def login():
    form = LoginForm()

    if form.validate():
        email = form.email.data
        password = form.password.data
        try:
            user = User.query.filter_by(email = email).first()

            if user and user.check_password(password):
                access_token = create_access_token(identity = user.id)
                refresh_token = create_refresh_token(identity = user.id)
                return jsonify({
                    "message": "User registered successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token
            })
            else:
                return jsonify({ 'message': 'Invalid credentials' }), 401
        except Exception as e:
            return jsonify({ 'message': 'An unexpected error occurred', 'error': str(e) }), 500
        
    return jsonify({ "message": "Validation failed", }), 500


@auth_router.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity = identity)
    return jsonify({"access_token": new_access_token})


@auth_router.route("/whoami")
@jwt_required()
def whoami():
    return jsonify({"claims": get_jwt()})
