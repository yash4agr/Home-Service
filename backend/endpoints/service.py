from flask import Blueprint, jsonify, request, json
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
import os
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.models import db, UserLogin, UserAddress, Professional, Services, Category
from forms import ServiceForm
from utils import handle_image_upload, handle_image_delete

service_router = Blueprint("service", __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = UserLogin.query.get(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({"message": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

@service_router.route("/services/categories", methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@service_router.route("/services", methods=['GET'])
def get_services():
    services = Services.query.all()
    return jsonify([service.to_dict() for service in services])


@service_router.route("/services", methods=['POST', 'PUT'])
@jwt_required()
@admin_required
def create_or_update_service():
    try:
        service_id = request.args.get('service_id')
        form = ServiceForm(request.form)
        
        # Populate category choices
        categories = Category.query.all()
        form.category_id.choices = [(c.id, c.name) for c in categories]
        if form.validate():
            # Handle new category creation
            category_id = None
            if form.new_category.data:
                category = Category.query.filter_by(name=form.new_category.data).first()
                if not category:
                    category = Category(name=form.new_category.data)
                    db.session.add(category)
                    db.session.flush()
                category_id = category.id
            else:
                category_id = form.category_id.data

            # Handle service creation/update
            if service_id:
                service = Services.query.get(service_id)
                if not service:
                    return jsonify({"message": "Service not found"}), 404
            else:
                service = Services()
            
            # Update service attributes
            service.name = form.name.data
            service.description = form.description.data
            service.base_price = form.base_price.data
            service.time_required = form.time_required.data
            service.category_id = category_id
            
            # Handle image upload
            if 'img' in request.files and request.files['img'].filename:
                new_path = handle_image_upload(request.files['img'], service_id)
                service.img = new_path
            
            # Handle tags
            tags_data = request.form.get('tags')
            if tags_data:
                service.tags = json.loads(tags_data)
            
            if not service_id:
                db.session.add(service)
            
            db.session.commit()
            return jsonify(service.to_dict()), 200 if service_id else 201
            
        return jsonify({"message": "Validation error", "errors": form.errors}), 422
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@service_router.route("/services/<int:service_id>", methods=['DELETE'])
@jwt_required()
@admin_required
def delete_service(service_id):
    try:
        service = Services.query.get(service_id)

        if not service:
            return jsonify({"message": "Service not found"}), 404
        
        if service.img:
            try:
                handle_image_delete(service.img)
            except OSError:
                pass 
        
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({"message": "Service deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500