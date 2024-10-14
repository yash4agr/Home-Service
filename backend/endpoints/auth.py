from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token , jwt_required, get_jwt_identity, get_jwt

from database.models import db, UserLogin, UserAddress
from forms import RegistrationForm, LoginForm

auth_router = Blueprint("auth", __name__)


# Routes
@auth_router.route("/register", methods=["POST"], endpoint="auth-register")
def register():
    
    form = RegistrationForm()

    # Validate form
    if not form.validate():
        jsonify({ "message": "Invalid form data" }), 400

    email = form.email.data
    password = form.password.data

    # Check if user already exist
    if UserLogin().validate_email(email):
        return jsonify({ "message": "User with this email already exists" }), 400
    
    new_user = UserLogin(email=email)
    new_user.set_password(password)

    try:
        # Add user to database and login
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity = new_user.id)
        refresh_token = create_refresh_token(identity = new_user.id)
        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500

@auth_router.route("/login", methods=["POST"], endpoint="auth-login")
def login():
    form = LoginForm()

    # Validate form
    if not form.validate():
        jsonify({ "message": "Invalid form data" }), 400

    email = form.email.data
    password = form.password.data

    try:
        user = UserLogin.query.filter_by(email = email).first()

        # Validate user credentials and login
        if user and user.check_password(password):
            access_token = create_access_token(identity = user.id)
            refresh_token = create_refresh_token(identity = user.id)
            return jsonify({
                "message": "Login successfully",
                "access_token": access_token,
                "refresh_token": refresh_token
                })
        else:
            return jsonify({ 'message': 'Invalid credentials' }), 401
        
    except Exception as e:
        return jsonify({ 'message': 'An unexpected error occurred', 'error': str(e) }), 500
    

@auth_router.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user = UserLogin.query.filter_by(user_id = get_jwt_identity()).first()

    if not user:
        return jsonify({ "message": "User not found" }), 404
    
    return jsonify({
        "name": user.name,
        "email" : user.email,
        "is_email_verified" : user.is_email_verified,
        "phone_number": user.phone_number,
        "is_phone_verified": user.is_phone_verified
    })


@auth_router.route("/address", methods=["GET", "POST"])
@jwt_required()
def address():
    user = UserLogin.query.filter_by(user_id = get_jwt_identity()).first()

    if not user:
        return jsonify({ "message": "User not found" }), 404

    if request.method == "GET":
        addresses = UserAddress.query.filter_by(user_login_id=user.id).all()
        return jsonify([{
            "id": addr.id,
            "address_type": addr.address_type,
            "street": addr.street,
            "city": addr.city,
            "state": addr.state,
            "zip_code": addr.zip_code,
            "country": addr.country
        } for addr in addresses])

    if request.method == "POST":
        form = AddressUpdateForm()
        if form.validate():
            new_address = UserAddress(
                user_login_id=user.id,
                address_type=form.address_type.data,
                street=form.street.data,
                city=form.city.data,
                state=form.state.data,
                zip_code=form.zip_code.data,
                country=form.country.data
            )
            try:
                # Add address to database
                db.session.add(new_address)
                db.session.commit()
                return jsonify({"message": "Address added successfully"}), 201
        
            except Exception as e:
                db.session.rollback()
                return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500



@auth_router.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    try:
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity = identity)
        return jsonify({"access_token": new_access_token})
    except Exception as e:
        return jsonify({ 'message': 'An unexpected error occurred', 'error': str(e) }), 500


@auth_router.route("/whoami")
@jwt_required()
def whoami():
    return jsonify({"claims": get_jwt()})
