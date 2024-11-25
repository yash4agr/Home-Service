from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, ForeignKey, func, event
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserLogin(db.Model):
    __tablename__ = 'user_login'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(10), nullable=False, default="user")

    phone_number = db.Column(db.String(20), nullable=True, unique=True)
    is_email_verified = db.Column(db.Boolean, default=False)

    is_banned = db.Column(db.Boolean, default=False)

    is_social_login = db.Column(db.Boolean, default=False)
    social_provider = db.Column(db.String(25), default='email')
    social_id = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    user_addresses = db.relationship("UserAddress", back_populates="user_login", cascade="all, delete-orphan")

    def validate_email(self, email):
        return self.query.filter_by(email=email).first() is not None

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        if self.password:
            return check_password_hash(self.password, password)
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_banned': self.is_banned,
            'is_email_verified': self.is_email_verified,
            'phone_number': self.phone_number,
            'created_at': self.created_at,
        }
    

class UserAddress(db.Model):
    __tablename__ = 'user_addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_login_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), nullable=False)
    address_type = db.Column(db.String(20), nullable=False, default="user")
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False, default="India")
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    user_login = db.relationship("UserLogin", back_populates="user_addresses")

    def to_dict(self):
        return {
            'id': self.id,
            'address_type': self.address_type,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'pin_code': self.zip_code,
            'country': self.country,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    services = db.relationship('Services', backref='category', lazy=True)
    professionals = relationship('Professional', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Services(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(255), nullable=False, default='img/default_service.jpg')
    time_required = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    tags = db.Column(db.JSON)
    avg_rating = db.Column(db.Float, default=0.0)
    total_requests = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_price': self.base_price,
            'img': 'http://localhost:5000/'+self.img,
            'time_required': self.time_required,
            'category_id': self.category_id,
            'tags': self.tags or [],
            'rating': self.avg_rating,
            'total_requests':self.total_requests,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update_rating(self):
        
        result = db.session.query(
            func.avg(ServiceRequest.rating).label('avg_rating'),
            func.count(ServiceRequest.id).label('total_requests')
        ).filter(
            ServiceRequest.service_id == self.id,
            ServiceRequest.status == 'completed',
            ServiceRequest.rating.isnot(None)
        ).first()
        
        self.avg_rating = result.avg_rating or 0.0
        self.total_requests = result.total_requests or 0

class Professional(db.Model):
    __tablename__  = 'professionals'

    id = db.Column(db.Integer, primary_key=True)
    user_login_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    resume_path = db.Column(db.String(255), nullable=True)
    avg_rating = db.Column(db.Float, default=0.0)
    total_services = db.Column(db.Integer, default=0)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user_login = db.relationship("UserLogin", backref=db.backref("professionals", uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category_id,
            'experience': self.experience,
            'resume_path': 'http://localhost:5000/'+self.resume_path,
            'rating':self.avg_rating,
            'total_services':self.total_services,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update_rating(self):
        result = db.session.query(
            func.avg(ServiceRequest.rating).label('avg_rating'),
            func.count(ServiceRequest.id).label('total_services')
        ).filter(
            ServiceRequest.professional_id == self.id,
            ServiceRequest.status == 'completed',
            ServiceRequest.rating.isnot(None)
        ).first()
        
        self.avg_rating = result.avg_rating or 0.0
        self.total_services = result.total_services or 0

class ServiceRequest(db.Model):
    __tablename__  = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('user_addresses.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="requested")
    date_of_request = db.Column(db.DateTime(timezone=True), nullable=False)
    date_of_completion = db.Column(db.DateTime(timezone=True), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    service = db.relationship("Services", backref='service_requests')
    customer = db.relationship("UserLogin", foreign_keys=[customer_id], backref='service_requests')
    professional = db.relationship("Professional", backref='service_requests')
    address = db.relationship("UserAddress", backref='service_requests')

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'date_of_request': self.date_of_request.isoformat(),
            'date_of_completion': self.date_of_completion.isoformat(),
            'rating':self.rating,
            'total_reviewservices':self.review,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def complete_service(self, rating, review=None):
        """Complete the service request with rating and review"""
        self.status = 'completed'
        self.date_of_completion = datetime.now(timezone.utc)
        self.rating = rating
        self.review = review
        
        # Update average ratings
        self.service.update_rating()
        self.professional.update_rating()

class ServiceStats(db.Model):
    __tablename__ = 'service_stats'

    id = db.Column(db.Integer, primary_key=True)
    total_users = db.Column(db.Integer, default=0)
    total_professionals = db.Column(db.Integer, default=0)
    total_services = db.Column(db.Integer, default=0)
    total_completed_requests = db.Column(db.Integer, default=0)
    total_pending_requests = db.Column(db.Integer, default=0)
    total_expired_requests = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc))

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance of ServiceStats"""
        stats = cls.query.first()
        if not stats:
            stats = cls()
            db.session.add(stats)
            db.session.commit()
        return stats
    
    @classmethod
    def update_stats(cls):
        """Update service statistics"""
        stats = cls.get_instance()
        
        stats.total_users = UserLogin.query.filter_by(role='user').count()
        stats.total_professionals = Professional.query.filter_by(is_approved=True).count()
        stats.total_services = Services.query.count()
        
        # Update request counts
        stats.total_completed_requests = ServiceRequest.query.filter_by(status='completed').count()
        stats.total_pending_requests = ServiceRequest.query.filter_by(status='pending').count()
        stats.total_expired_requests = ServiceRequest.query.filter_by(status='expired').count()
        
        # Calculate average rating
        completed_requests = db.session.query(
            func.avg(ServiceRequest.rating).label('avg_rating')
        ).filter(
            ServiceRequest.status == 'completed',
            ServiceRequest.date_of_completion.isnot(None)
        ).first()
        
        stats.avg_rating = completed_requests.avg_rating or 0.0
        
        db.session.commit()

# @event.listens_for(ServiceRequest.status, 'set')
# def service_request_status_change(target, value, oldvalue, initiator):
#     """Listen for status changes in ServiceRequest"""
#     if value != oldvalue:
#         db.session.add(target)
#         @event.listens_for(db.session, 'after_commit')
#         def update_stats_after_commit(session):
#             ServiceStats.update_stats()
#             event.remove(db.session, 'after_commit', update_stats_after_commit)

# @event.listens_for(Professional, 'after_insert')
# def professional_created(mapper, connection, target):
#     """Listen for new professional creation"""
#     @event.listens_for(db.session, 'after_commit')
#     def update_stats_after_commit(session):
#         ServiceStats.update_stats()
#         event.remove(db.session, 'after_commit', update_stats_after_commit)

# @event.listens_for(Services, 'after_insert')
# def service_created(mapper, connection, target):
#     """Listen for new service creation"""
#     @event.listens_for(db.session, 'after_commit')
#     def update_stats_after_commit(session):
#         ServiceStats.update_stats()
#         event.remove(db.session, 'after_commit', update_stats_after_commit)

# @event.listens_for(UserLogin, 'after_insert')
# def user_created(mapper, connection, target):
#     """Listen for new user creation"""
#     if target.role == 'user':
#         @event.listens_for(db.session, 'after_commit')
#         def update_stats_after_commit(session):
#             ServiceStats.update_stats()
#             event.remove(db.session, 'after_commit', update_stats_after_commit)
