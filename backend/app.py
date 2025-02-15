# Import libraries
import os
from dotenv import load_dotenv
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
from endpoints.bookings import bookings_router

# Import database, stuff
from database.models import db, UserLogin
from celery_config import init_celery
from cache import cache
import redis

load_dotenv()

# Initialize Flask instance
app = Flask(__name__)

# Database Config
db_path = os.path.join(os.path.dirname(__file__), 'database', 'hsa.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path) # to-do, read from env file

# JWT config
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'someSecretKey')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Redis cache config
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = redis_host
app.config['CACHE_REDIS_PORT'] = redis_port
app.config['CACHE_REDIS_DB'] = 1

cache.init_app(app)

redis_client = redis.Redis(host=redis_host, port=redis_port, db=1, decode_responses=True)

jwt = JWTManager(app)

OLA_API_KEY = os.environ.get('OLA_API_KEY')

# Export files location
app.config['EXPORT_FOLDER'] = '/database/export_files'

app.config['CELERY_BROKER_URL'] = f'redis://{redis_host}:6379/2'
app.config['CELERY_RESULT_BACKEND'] = f'redis://{redis_host}:6379/3'

# Initialize database
db.init_app(app)


CORS(app, resources={r"/*": {"origins": "*"}})
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
        url = f"https://api.olamaps.io/places/v1/reverse-geocode?latlng={latitude},{longitude}&api_key={OLA_API_KEY}"

        # Make the request to Ola API
        response = requests.get(url)
        response.raise_for_status()

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
app.register_blueprint(bookings_router, url_prefix="/api/bookings")

# Create the tables if they don't exist
with app.app_context():
    db.create_all()

# Initialize Celery
celery = init_celery(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)