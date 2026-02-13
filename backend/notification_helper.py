"""
Helper function to send SMS notifications for violations
"""

def send_violation_notifications(violations_data, detections):
    """
    Send SMS notifications for all violations with identified license plates
    
    Args:
        violations_data: Violation analysis results
        detections: All detection objects
        
    Returns:
        list: SMS send results
    """
    notifications_sent = []
    
    if violations_data['total_violations'] == 0:
        return []
    
    # Extract license plates from detections
    license_plates = set()
    for detection in detections:
        if 'license_plate' in detection and detection['license_plate']:
            license_plates.add(detection['license_plate'])
    
    if not license_plates:
        print("⚠️ No license plates detected - cannot send SMS")
        return []
    
    # Send notification for each vehicle
    for plate in license_plates:
        # Lookup vehicle owner info
        vehicle_info = vehicle_db.get_vehicle_info(plate)
        
        if not vehicle_info:
            print(f"⚠️ Vehicle {plate} not found in database")
            notifications_sent.append({
                'license_plate': plate,
                'status': 'not_found',
                'message': 'Vehicle not registered in database'
            })
            continue
        
        phone_number = vehicle_info['phone']
        
        # Send SMS (or demo notification)
        if sms_service.enabled:
            result = sms_service.send_violation_sms(
                phone_number=phone_number,
                license_plate=plate,
                violations=violations_data['violations'],
                total_penalty=violations_data['total_penalty_range']
            )
        else:
            result = sms_service.send_demo_notification(
                phone_number=phone_number,
                license_plate=plate,
                violations=violations_data['violations'],
                total_penalty=violations_data['total_penalty_range']
            )
        
        result['license_plate'] = plate
        result['owner'] = vehicle_info.get('owner', 'Unknown')
        notifications_sent.append(result)
    
    return notifications_sent
