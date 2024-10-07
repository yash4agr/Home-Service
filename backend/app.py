# Import libraries
import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Import endpoints
from endpoints.auth import auth_router

# Import database, stuff
from database.models import db, UserLogin


# Initialize Flask instance
app = Flask(__name__)

# Database Config
db_path = os.path.join(os.path.dirname(__file__), 'database', 'hsa.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path) # to-do, read from env file

# JWT config
app.config['JWT_SECRET_KEY'] = "someSecretKey" # to-do, read from env file
jwt = JWTManager(app)


# Initialize database
db.init_app(app)

CORS(app)
app.config['WTF_CSRF_ENABLED'] = False

# Additional JWT claims
@jwt.additional_claims_loader
def make_additional_claims(identity):
        return jsonify({"role": UserLogin.query.filter_by(id = identity).first().role})

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message":"Token has expired", "error":"token_expired"})

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message":"Signature verification failed", "error":"invalid_token"})

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message":"Request doesn't contain valid token", "error":"authorization_failed"})



# Register the router
app.register_blueprint(auth_router, url_prefix = '/api/auth')

# Create the tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)