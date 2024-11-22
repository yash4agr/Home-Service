from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token , jwt_required, get_jwt_identity, get_jwt

from database.models import db, UserLogin, UserAddress
from forms import RegistrationForm, LoginForm, ResetPasswordForm
from utils import generate_otp, store_otp, get_stored_otp, send_otp_email

auth_router = Blueprint("auth", __name__)


# Routes
@auth_router.route("/register", methods=["POST"], endpoint="auth-register")
def register():
    
    form = RegistrationForm(request.form)
    # Validate form
    if not form.validate():
        return jsonify({ "message": "Invalid form data" }), 400

    name = form.name.data
    email = form.email.data
    password = form.password.data

    # Check if user already exist
    if UserLogin().validate_email(email):
        return jsonify({ "message": "User with this email already exists" }), 400
    
    new_user = UserLogin(email=email, name=name)
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
            "refresh_token": refresh_token,
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role,
                "isVerified": new_user.is_email_verified,
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500

@auth_router.route("/login", methods=["POST"], endpoint="auth-login")
def login():
    form = LoginForm(request.form)

    # Validate form
    if not form.validate():
        return jsonify({ "message": "Invalid form data" }), 400

    email = form.email.data
    password = form.password.data

    try:
        user = UserLogin.query.filter_by(email = email).first()

        # Validate user credentials and login
        if user and user.check_password(password):
            access_token = create_access_token(identity = user.id)
            refresh_token = create_refresh_token(identity = user.id)
            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "is_email_verified": user.is_email_verified
                }
            })
        else:
            return jsonify({ 'message': 'Invalid credentials' }), 401
        
    except Exception as e:
        return jsonify({ 'message': 'An unexpected error occurred', 'error': str(e) }), 500

@auth_router.route("/google-login", methods=["POST"])
def google_login():
    userData = request.json.get('userData')
    if not userData:
        return jsonify({"message": "User data provided"}), 400

    try: 

        email = userData.get('email')
        name = userData.get('name')
        google_id = userData.get('sub')
        # Check if user exists
        user = UserLogin.query.filter_by(email=email).first()

        if not user:
            user = UserLogin(
                email=email, 
                name=name, 
                is_social_login=True,
                social_provider='google',
                social_id=google_id,
                is_email_verified=True 
            )
            db.session.add(user)
            db.session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_email_verified": user.is_email_verified
            }
        }), 200
    except Exception as e:
        return jsonify({"message": "Authentication failed", "error": str(e)}), 500


@auth_router.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    verification_type = data.get('type')

    if not email or not otp or not verification_type:
        return jsonify({
            "message": "Missing required parameters",
            "verified": False
        }), 400

    stored_otp = get_stored_otp(email, verification_type)
    
    if not stored_otp:
        return jsonify({
            "message": "OTP expired or not found",
            "verified": False
        }), 400

    if otp == stored_otp.decode('utf-8'):
        user = UserLogin.query.filter_by(email=email).first()
        
        if verification_type == 'email-verification':
            user.is_email_verified = True
        
        db.session.commit()

        return jsonify({
            "message": "OTP verified successfully",
            "verified": True,
            # Add any additional user data if needed
        }), 200
    else:
        return jsonify({
            "message": "Invalid OTP",
            "verified": False
        }), 400

    # return jsonify({
    #         "message": "OTP verified successfully",
    #         "verified": True,
    #         # Add any additional user data if needed
    #     }), 200

@auth_router.route("/resend-otp", methods=["POST"])
def resend_otp():
    data = request.get_json()
    email = data.get('email')
    verification_type = data.get('type')

    if not email or not verification_type:
        return jsonify({
            "message": "Missing email or verification type",
        }), 400

    # Check if user exists
    user = UserLogin.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            "message": "User not found",
        }), 404

    # Generate new OTP
    new_otp = generate_otp()
    
    # Store new OTP
    store_otp(email, new_otp, verification_type)
    
    # Send OTP via email
    try:
        send_otp_email(email, new_otp)
    except Exception as e:
        # Log the error
        print(f"Email sending failed: {str(e)}")
        return jsonify({
            "message": "Failed to send OTP. Please try again.",
        }), 500

    return jsonify({
        "message": "New OTP sent successfully"
    }), 200

@auth_router.route("/reset-password", methods=["POST"])
def reset_password():
    form = ResetPasswordForm(request.form)

    if not form.validate():
        return jsonify({ "message": "Invalid form data" }), 400

    email = form.email.data
    password = form.password.data

    try:
        user = UserLogin.query.filter_by(email=email).first()
        if not user:
            return jsonify({ "message": "User not found" }), 404

        user.set_password(password)
        db.session.commit()

        return jsonify({
            "message": "Password reset successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({ "message": "An error occurred", "error": str(e) }), 500

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
