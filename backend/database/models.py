from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship
# from sqlalchemy import DateTime, ForeignKey
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserLogin(db.Model):
    __tablename__ = 'user_login'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True) # Nullable for social login
    role = db.Column(db.String(10), nullable=False, default="user")

    is_social_login = db.Column(db.Boolean, default=False)
    social_provider = db.Column(db.String(25), default='email')
    social_id = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    is_flagged = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)

    is_email_verified = db.Column(db.Boolean, default=False)

    # Relationships
    profile = db.relationship("UserProfile", back_populates="user_login", uselist=False)

    def validate_email(self, email):
        return self.query.filter_by(email=email).first() is not None

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    user_login_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), unique=True, nullable=False)
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    phone_number = db.Column(db.String(20), nullable=True, unique=True)
    is_phone_verified = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship
    user_login = db.relationship("UserLogin", back_populates="profile")
    user_addresses = db.relationship("UserAddress", back_populates="user_profile", cascade="all, delete-orphan")

class UserAdress(db.Model):
    __tablename__ = 'user_addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    address_type = db.Column(db.String(20), nullable=False, default="home")
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False, default="India")
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    user_profile = db.relationship("UserProfile", back_populates="user_addresses")

class Services(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(255), nullable=False,  default='PATH/TO_IMG.jpg')
    time_required = db.Column(db.Integer, nullable=False)

    available = db.Column(db.String(100), nullable=False) # Column type will change

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    service = db.relationship("Service", back_populates="faqs")

class Professional(db.Model):
    __tablename__  = 'professionals'

    id = db.Column(db.Integer, primary_key=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user_profile = db.relationship("UserProfile", backref=db.backref("professionals", uselist=False))
    service = db.relationship("Service", backref='professionals')

class ServiceRequest(db.Model):
    __tablename__  = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    date_of_request = db.Column(db.DateTime(timezone=True), nullable=False)
    date_of_completion = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="requested")
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    service = db.relationship("Service", backref='service_requests')
    customer = db.relationship("UserProfile", foreign_keys=[customer_id], backref='service_requests')
    professional = db.relationship("Professional", backref='service_requests')

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    rating = db.Column(db.Interger, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    service_request = db.relationship("ServiceRequest", backref='reviews')
    professional = db.relationship("Professional", backref='service_requests')
