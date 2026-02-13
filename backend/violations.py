"""
Enhanced Traffic Violation Detection Module with Video Support
"""

import numpy as np
from collections import defaultdict, deque

# (Previous VIOLATIONS dict remains the same...)
VIOLATIONS = {
    'NO_HELMET': {
        'name': 'Riding Without Helmet',
        'severity': 'High',
        'penalty': '₹1,000',
        'section': 'Section 129, Motor Vehicles Act',
        'description': 'Two-wheeler rider/pillion rider without helmet'
    },
    'RED_LIGHT': {
        'name': 'Red Light Violation',
        'severity': 'High',
        'penalty': '₹1,000',
        'section': 'Section 177, Motor Vehicles Act',
        'description': 'Crossing traffic signal during red light'
    },
    'TRIPLE_RIDING': {
        'name': 'Triple Riding',
        'severity': 'High',
        'penalty': '₹1,000',
        'section': 'Section 128, Motor Vehicles Act',
        'description': 'More than 2 persons on a two-wheeler'
    },
    'OVERSPEEDING': {
        'name': 'Overspeeding',
        'severity': 'Medium',
        'penalty': '₹1,000-₹2,000',
        'section': 'Section 183, Motor Vehicles Act',
        'description': 'Exceeding speed limit'
    }
}

# (All previous detection functions remain the same...)
def boxes_overlap(box1, box2, iou_threshold=0.1):
    """Check if two bounding boxes overlap"""
    x1_1, y1_1, x2_1, y2_1 = box1
    x1_2, y1_2, x2_2, y2_2 = box2
    
    x1_i = max(x1_1, x1_2)
    y1_i = max(y1_1, y1_2)
    x2_i = min(x2_1, x2_2)
    y2_i = min(y2_1, y2_2)
    
    if x2_i < x1_i or y2_i < y1_i:
        return False
    
    intersection = (x2_i - x1_i) * (y2_i - y1_i)
    area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
    
    iou = intersection / (area1 + area2 - intersection)
    return iou > iou_threshold

def point_in_box(point, box, margin=50):
    """Check if point is inside or near box"""
    x, y = point
    x1, y1, x2, y2 = box
    return (x1 - margin < x < x2 + margin and 
            y1 - margin < y < y2 + margin)

def detect_helmet_violation(detections):
    """Detect helmet violations"""
    violations = []
    
    has_no_helmet_class = any(d['class'].lower() in ['no-helmet', 'no_helmet', 'without-helmet', 'without_helmet'] 
                               for d in detections)
    
    if has_no_helmet_class:
        for detection in detections:
            if detection['class'].lower() in ['no-helmet', 'no_helmet', 'without-helmet', 'without_helmet']:
                violation = {
                    'type': 'NO_HELMET',
                    'detection': detection,
                    **VIOLATIONS['NO_HELMET']
                }
                violations.append(violation)
    else:
        motorcycles = [d for d in detections if d['class'] in ['motorcycle', 'bicycle']]
        persons = [d for d in detections if d['class'] == 'person']
        
        for vehicle in motorcycles:
            v_bbox = vehicle['bbox']
            v_center_x = (v_bbox[0] + v_bbox[2]) / 2
            v_center_y = (v_bbox[1] + v_bbox[3]) / 2
            
            riders_on_vehicle = []
            for person in persons:
                p_bbox = person['bbox']
                p_center_x = (p_bbox[0] + p_bbox[2]) / 2
                p_center_y = (p_bbox[1] + p_bbox[3]) / 2
                
                if point_in_box((p_center_x, p_center_y), v_bbox, margin=80):
                    riders_on_vehicle.append(person)
            
            if riders_on_vehicle:
                violation = {
                    'type': 'NO_HELMET',
                    'detection': riders_on_vehicle[0],
                    'vehicle_detection': vehicle,
                    'note': 'Detected with generic model - visual verification recommended',
                    **VIOLATIONS['NO_HELMET']
                }
                violations.append(violation)
    
    return violations

def detect_triple_riding(detections):
    """Detect triple riding"""
    violations = []
    
    motorcycles = [d for d in detections if d['class'] in ['motorcycle', 'bicycle']]
    persons = [d for d in detections if d['class'] == 'person']
    
    for vehicle in motorcycles:
        v_bbox = vehicle['bbox']
        
        riders_on_vehicle = []
        for person in persons:
            p_bbox = person['bbox']
            p_center_x = (p_bbox[0] + p_bbox[2]) / 2
            p_center_y = (p_bbox[1] + p_bbox[3]) / 2
            
            if point_in_box((p_center_x, p_center_y), v_bbox, margin=80):
                riders_on_vehicle.append(person)
        
        if len(riders_on_vehicle) > 2:
            violation = {
                'type': 'TRIPLE_RIDING',
                'detection': vehicle,
                'rider_count': len(riders_on_vehicle),
                'riders': riders_on_vehicle,
                **VIOLATIONS['TRIPLE_RIDING'],
                'description': f'{len(riders_on_vehicle)} persons detected on two-wheeler (max allowed: 2)'
            }
            violations.append(violation)
    
    return violations

def detect_red_light_violation(detections):
    """Detect red light violations"""
    violations = []
    
    red_lights = [d for d in detections 
                  if d['class'].lower() in ['traffic-light-red', 'traffic_light_red', 'red_light', 'red-light']]
    
    if not red_lights:
        return violations
    
    vehicles = [d for d in detections 
                if d['class'] in ['car', 'truck', 'bus', 'motorcycle', 'bicycle']]
    
    for red_light in red_lights:
        rl_bbox = red_light['bbox']
        rl_bottom = rl_bbox[3]
        
        for vehicle in vehicles:
            v_bbox = vehicle['bbox']
            v_top = v_bbox[1]
            
            if v_top > rl_bottom:
                violation = {
                    'type': 'RED_LIGHT',
                    'detection': vehicle,
                    'traffic_light': red_light,
                    **VIOLATIONS['RED_LIGHT']
                }
                violations.append(violation)
                break
    
    return violations

def detect_overspeeding_from_video_frames(tracked_vehicles, fps, speed_limit=60):
    """
    Detect overspeeding from tracked vehicles across video frames
    
    Args:
        tracked_vehicles: Dict of {vehicle_id: [(frame_num, bbox), ...]}
        fps: Video frame rate
        speed_limit: Speed limit in km/h
        
    Returns:
        List of speeding violations
    """
    violations = []
    
    # This is a simplified implementation
    # In production, would use proper object tracking (DeepSORT/ByteTrack)
    # and camera calibration for accurate speed measurement
    
    for vehicle_id, trajectory in tracked_vehicles.items():
        if len(trajectory) < 2:
            continue
        
        # Calculate approximate speed based on bbox movement
        # This is VERY approximate without proper calibration
        first_frame, first_bbox = trajectory[0]
        last_frame, last_bbox = trajectory[-1]
        
        # Calculate pixel distance traveled
        x1_center = (first_bbox[0] + first_bbox[2]) / 2
        y1_center = (first_bbox[1] + first_bbox[3]) / 2
        x2_center = (last_bbox[0] + last_bbox[2]) / 2
        y2_center = (last_bbox[1] + last_bbox[3]) / 2
        
        pixel_distance = np.sqrt((x2_center - x1_center)**2 + (y2_center - y1_center)**2)
        
        # Time elapsed
        time_elapsed = (last_frame - first_frame) / fps
        
        if time_elapsed > 0 and pixel_distance > 50:  # Minimum movement threshold
            # This would need proper calibration
            # For now, flag as "potential speeding - needs verification"
            violation = {
                'type': 'OVERSPEEDING',
                'vehicle_id': vehicle_id,
                'pixel_speed': pixel_distance / time_elapsed,
                'note': 'Approximate detection - requires camera calibration for  accurate speed',
                **VIOLATIONS['OVERSPEEDING']
            }
            violations.append(violation)
    
    return violations

def analyze_violations(detections, model_names, image_shape=None):
    """Main violation analysis function"""
    all_violations = []
    
    # Detect helmet violations
    helmet_violations = detect_helmet_violation(detections)
    all_violations.extend(helmet_violations)
    
    # Detect triple riding
    triple_riding_violations = detect_triple_riding(detections)
    all_violations.extend(triple_riding_violations)
    
    # Detect red light violations
    red_light_violations = detect_red_light_violation(detections)
    all_violations.extend(red_light_violations)
    
    # Calculate summary
    violation_breakdown = {}
    for violation in all_violations:
        v_type = violation['type']
        violation_breakdown[v_type] = violation_breakdown.get(v_type, 0) + 1
    
    summary = {
        'total_violations': len(all_violations),
        'violation_types': violation_breakdown,
        'violations': all_violations,
        'total_penalty_range': calculate_total_penalty(all_violations)
    }
    
    return summary

def calculate_total_penalty(violations):
    """Calculate total penalty amount"""
    if not violations:
        return "₹0"
    
    total = 0
    for v in violations:
        penalty_str = v['penalty']
        import re
        numbers = re.findall(r'[\d,]+', penalty_str.replace(',', ''))
        if numbers:
            total += int(numbers[0])
    
    return f"₹{total:,}"
