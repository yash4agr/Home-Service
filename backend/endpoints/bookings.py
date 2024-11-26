from flask import Blueprint, jsonify, request
import flask 
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
from database.models import (db, 
                            UserLogin,
                            UserAddress, 
                            Professional, 
                            Services,
                            ServiceRequest)
from forms import BookingRequestForm


bookings_router = Blueprint("bookings", __name__)

@bookings_router.route('/check-serviceability', methods=['GET'])
def check_serviceability():
    pincode = request.args.get('pincode')
    service_ids = request.args.get('serviceIds', '').split(',')
    
    try:
        if not pincode or not service_ids:
            return jsonify({
                'serviceable': False, 
                'message': 'Invalid pincode or services'
            }), 400
        
        # Convert service_ids to integers
        service_ids = [int(sid) for sid in service_ids if sid.strip()]
        
        # Check serviceability for each service
        serviceable_services = []
        for service_id in service_ids:
            service = Services.query.get(service_id)
            if not service:
                return jsonify({
                    'serviceable': False, 
                    'message': f'Service {service_id} not found'
                }), 400
            
            professional_exists = Professional.query.join(UserLogin) \
                .join(UserAddress) \
                .filter(
                    Professional.category_id == service.category_id,
                    Professional.is_approved == True,
                    UserAddress.zip_code == pincode
                ).first()
            
            if not professional_exists:
                return jsonify({
                    'serviceable': False, 
                    'message': f'No professionals available for service {service_id} in pincode {pincode}'
                }), 400
            
            serviceable_services.append(service_id)

        return jsonify({
            'serviceable': True, 
            'serviceable_services': serviceable_services,
            'message': 'Services are available in this area'
        })
    
    except SQLAlchemyError as e:
        return jsonify({
            'serviceable': False, 
            'message': str(e)
        }), 500
    except ValueError:
        return jsonify({
            'serviceable': False, 
            'message': 'Invalid service ID format'
        }), 400

@bookings_router.route('/create_booking', methods=['POST'])
@jwt_required()
def create_booking():
    form = BookingRequestForm(formdata=request.form)
    services_data = []
    i = 0
    while f'services[{i}][service_id]' in request.form:
        services_data.append({
            'service_id': request.form.get(f'services[{i}][service_id]'),
            'hours': request.form.get(f'services[{i}][hours]'),
            'base_price': request.form.get(f'services[{i}][base_price]')
        })
        i += 1

    if not form.validate():
        print(form.errors)
        return jsonify({
            'message': 'Validation failed', 
            'errors': form.errors
        }), 400
    
    try:
        current_user_id = get_jwt_identity()
        # Create or find user address
        address = UserAddress(
            user_login_id=current_user_id,
            address_type='service',
            street=form.locality.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.pincode.data
        )
        db.session.add(address)
        db.session.flush()

        user = UserLogin.query.get(current_user_id)
        user.phone_number = form.phone_number.data
        db.session.add(user)
        
        # Prepare service requests
        service_requests = []
        for service_data in services_data:
            service = Services.query.get(service_data['service_id'])
            if not service:
                raise ValueError(f"Service {service_data['service_id']} not found")
            
            service_datetime = datetime.combine(
                            form.service_date.data.date(), 
                            datetime.strptime(form.service_time.data, '%H:%M').time()
                        ).replace(tzinfo=timezone.utc)
            
            service_request = ServiceRequest(
                service_id=service.id,
                customer_id=current_user_id,
                professional_id=None,
                address_id=address.id,
                date_of_request=service_datetime,
                status='pending',
            )
            service_requests.append(service_request)
        
        # Add all service requests
            db.session.add(service_request)
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully', 
            'booking_ids': [req.id for req in service_requests]
        }), 201
    
    except (SQLAlchemyError, ValueError) as e:
        db.session.rollback()
        return jsonify({
            'message': str(e)
        }), 500


@bookings_router.route('/get_bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    current_user_id = get_jwt_identity()
    status = flask.request.args.get('status', default=None)
    # professional_id = request.args.get('professional_id', None)
    
    # Base query for service requests
    query = ServiceRequest.query.filter_by(customer_id=current_user_id)
    
    # if status:
    #     query = query.filter_by(status=status)
    
    # Fetch service requests with related data
    service_requests = query.all()
    
    booking_details = []
    for request in service_requests:
        booking_info = {
            'id': request.id,
            'service': request.service.to_dict(),
            'status': request.status,
            'date_of_request': request.date_of_request.isoformat(),
            'address': request.address.to_dict(),
            'customer_details': {
                    'name': request.customer.name,
                    'phone': request.customer.phone_number},
            'professional_details': None,
            'review_details': None
        }
        
        # Add professional details if service is accepted
        if request.professional:
            booking_info['professional_details'] = {
                'name': request.professional.user_login.name,
                'phone': request.professional.user_login.phone_number
            }
        
        # Add review details if service is completed
        if request.status == 'completed':
            booking_info['date_of_completion'] = request.date_of_completion
            booking_info['review_details'] = {
                'rating': request.rating,
                'review': request.review
            }
        
        booking_details.append(booking_info)
    
    return booking_details, 200
    
@bookings_router.route('/submit_review', methods=['POST'])
@jwt_required()
def submit_review():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    service_request_id = data.get('service_request_id')
    rating = data.get('rating')
    review_text = data.get('review')
    
    service_request = ServiceRequest.query.filter_by(
        id=service_request_id, 
        customer_id=current_user_id
    ).first()
    
    if not service_request:
        return jsonify({'message': 'Service request not found'}), 404
    
    if service_request.status != 'completed':
        return jsonify({'message': 'Can only review completed services'}), 400
    
    # Update review
    service_request.rating = rating
    service_request.review = review_text
    
    # Update service and professional ratings
    service_request.service.update_rating()
    service_request.professional.update_rating()
    
    db.session.commit()
    
    return jsonify({'message': 'Review submitted successfully'}), 200


    


def check_all_rejected(service_request):
    customer_address = service_request.address
    total_professionals = Professional.query.join(UserLogin).join(UserAddress).filter(
        and_(
            Professional.service_id == service_request.service_id,
            UserAddress.zip_code == customer_address.zip_code
        )
    ).count()

    rejections_count = ServiceRequestRejection.query.filter_by(service_request_id=service_request.id).count()

    return total_professionals == rejections_count