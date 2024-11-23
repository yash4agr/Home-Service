# Import libraries
import os
import requests
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

# Import endpoints
from endpoints.auth import auth_router
from endpoints.admin import admin_router
from endpoints.professional import professional_router
from endpoints.service import service_router

# Import database, stuff
from database.models import db, UserLogin


# Initialize Flask instance
app = Flask(__name__)

# Database Config
db_path = os.path.join(os.path.dirname(__file__), 'database', 'hsa.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path) # to-do, read from env file

# JWT config
app.config['JWT_SECRET_KEY'] = "someSecretKey" # to-do, read from env file
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)


# Initialize database
db.init_app(app)

CORS(app)
app.config['WTF_CSRF_ENABLED'] = False


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message":"Token has expired", "error":"token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message":"Signature verification failed", "error":"invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message":"Request doesn't contain valid token", "error":"authorization_failed"}), 401

@app.route('/get-location', methods=['POST'])
def get_location():
    try:
        # Get coordinates from the frontend
        data = request.json
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Construct the Ola API URL
        url = f"https://api.olamaps.io/places/v1/reverse-geocode?latlng={latitude},{longitude}&api_key=TdZk7h7BkXqq1rlcmlkGnGSYgPDqo3TlQaMWzBoR"

        # Make the request to Ola API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP codes like 4XX/5XX

        # Send the result back to the frontend
        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ola API: {e}")
        return jsonify({"error": "Failed to retrieve location data"}), 500



# Register the router
app.register_blueprint(auth_router, url_prefix = '/api/auth')
app.register_blueprint(admin_router, url_prefix = '/api/admin')
app.register_blueprint(professional_router, url_prefix="/api/professionals")
app.register_blueprint(service_router, url_prefix="/api")

# Create the tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)