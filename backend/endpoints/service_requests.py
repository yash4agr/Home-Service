from flask import Blueprint, jsonify, request
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from database.models import (db, 
                            UserLogin,
                            UserAddress, 
                            Professional, 
                            ServiceRequestRejection, 
                            ServiceRequest)
from forms import ServiceRequestForm


request_router = Blueprint("service_requests", __name__)

# Create a service
@request_router.route('/service_request', methods=['POST', 'PUT'])
def manage_service_request():
    form = ServiceRequestForm(request.json)
    if form.validate():
        try:
            request_id = request.args.get('request_id')
            if request.method == 'PUT':
                if not request_id:
                    return jsonify({"message": "Request ID is required for updates"}), 400
                service_request = ServiceRequest.query.get(request_id)
                if not service_request:
                    return jsonify({"message": f"No service found with id: {request_id}"}), 404
                if service_request.status != "requested":
                    return jsonify({"message": "Cannot update a service request that is not in 'requested' status"}), 400
                
                form.populate_obj(service_request)
            else:
                service_request = ServiceRequest()
                form.populate_obj(service_request)
                service_request.status = "requested"
                db.session.add(service_request)
            
            db.session.commit()
            return jsonify(service_request.to_dict()), 200 if request.method == 'PUT' else 201
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred while managing the service request", "error": str(e)}), 500
    return jsonify({"message": "Validation error", "errors": form.errors}), 422


@request_router.route('/service_request', methods=['GET'])
def get_service_request():
    request_id = request.args.get('request_id')
    if request_id:
        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return jsonify({"message": f"No service request found with id: { request_id }"}), 404
        return jsonify(service_request.to_dict())
    return jsonify({"message": "Request ID is required"}), 400
    

@request_router.route('/service_request/cancel', methods=['POST'])
def cancel_service_request():
    request_id = request.args.get('request_id')
    if not request_id:
        return jsonify({"message": "Request ID is required"}), 400
    
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"message": f"No service request found with id: { request_id }"}), 404
    
    if service_request.status not in ["requested", "pending"]:
        return jsonify({"message": "Service can not be cancelled"}), 400
    
    service_request.status = "cancelled"
    try:
        db.session.commit()
        return jsonify({"message": "Service request cancelled successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500
        
    


@request_router.route('/service_request/accept', methods=['POST'])
def accept_service_request():
    request_id = request.args.get('request_id')
    professional_id = request.args.get('professional_id')
    if not request_id:
        return jsonify({"message": "Request ID is required"}), 400
    if not professional_id:
        return jsonify({"message": "Professional ID is required"}), 400
    
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"message": f"No service request found with id: { request_id }"}), 404
    
    if service_request.status != "requested":
        return jsonify({"message": "This service request is no longer available"}), 400

    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": f"No professional found with id: { professional_id }"}), 404
    
    customer_address = service_request.address
    professional_user = UserAddress.query.get(professional.user_login_id)
    professional_address = professional_user.user_addresses[0]

    if customer_address.zip_code != professional_address.zip_code:
        return jsonify({"message": "Professional is not in the service area"}), 400
    
    try:
        service_request.professional_id = professional_id
        service_request.status = "pending"
        db.session.commit()
        return jsonify({"message": "Service request accepted successfully"}), 200
    
    except Exception as e:
        return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500
    

@request_router.route('/service_request/reject', methods=['POST'])
def reject_service_request():
    request_id = request.args.get('request_id')
    professional_id = request.args.get('professional_id')
    if not request_id:
        return jsonify({"message": "Request ID is required"}), 400
    if not professional_id:
        return jsonify({"message": "Professional ID is required"}), 400
    
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"message": f"No service request found with id: { request_id }"}), 404
    
    if service_request.status != "requested":
        return jsonify({"message": "This service request is no longer available"}), 400

    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"message": f"No professional found with id: { professional_id }"}), 404
    
    try:
        rejection = ServiceRequestRejection(service_request_id=request_id, professional_id=professional_id)
        db.session.add(rejection)
        db.session.commit()

        all_rejected = check_all_rejected(service_request)
        if all_rejected:
            db.session.commit()
            return jsonify({"message": "Service request rejected by all professionals"}), 200
        return jsonify({"message": "Service request rejected successfully"}), 200
    
    except Exception as e:
        return jsonify({ "message": "An internal error occurred", "error": str(e) }), 500
    


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