# Import libraries
import os
from flask import Flash
from flask_jwt_extended import JWTManager

# Import endpoints

# Import database, stuff
# from models import db


# Initialize Flask instance
app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hsa.sqlite3' # to-do, read from env file

# JWT config
app.config['JWT_SECRET_KEY'] = "someSecretKey" # to-do, read from env file
jwt = JWTManager(app)


# Initialize database
db.init_app(app)


# Register the router


# Create the tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)