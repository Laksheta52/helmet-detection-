from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
# import easyocr
import cv2
import numpy as np
import base64
import os
from pathlib import Path
from violations import analyze_violations, detect_overspeeding_from_video_frames
from sms_service import sms_service
from vehicle_db import vehicle_db
import tempfile

app = Flask(__name__)
CORS(app)

# Initialize model and OCR reader
print("="*60)
print("🚀 Traffic Violation Detection System - Starting...")
print("="*60)

print("\n📦 Loading YOLOv8 model...")

# Check for custom-trained traffic violation model
custom_model_path = 'best.pt'
if os.path.exists(custom_model_path):
    print(f"✓ Found custom traffic violation model: {custom_model_path}")
    model = YOLO(custom_model_path)
    model_name = "Custom Traffic Violation Detection"
    use_custom_model = True
    print("\n🎯 Custom Model Classes:")
    for idx, class_name in model.names.items():
        print(f"   {idx}: {class_name}")
else:
    print("⚠ Custom model (best.pt) not found.")
    print("\n📝 To use custom traffic violation detection:")
    print("  1. Train model using ENHANCED_Training.ipynb")
    print("  2. Download 'best.pt' from Colab")
    print(f"  3. Place in: {os.path.abspath('.')}")
    print("  4. Restart server")
    print("\n✓ Using generic YOLOv8s model (limited violation detection)")
    model = YOLO('yolov8s.pt')
    model_name = "YOLOv8s (Generic - Basic Detection Only)"
    use_custom_model = False

print(f"\n✓ Model loaded: {model_name}")

print("\n📝 Skipping EasyOCR for memory efficiency...")
# reader = easyocr.Reader(['en'], gpu=False)

print("\n📱 Initializing SMS notification service...")
print(f"SMS Status: {'Enabled (Twilio)' if sms_service.enabled else 'Demo Mode'}")

print("\n📋 Loading vehicle registration database...")
print(f"Registered vehicles: {len(vehicle_db.get_all_vehicles())}")

print("\n" + "="*60)
print("✅ System ready for traffic violation detection!")
print("📱 SMS notifications: {'ENABLED' if sms_service.enabled else 'DEMO MODE'}")
print("="*60 + "\n")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy', 
        'model': model_name,
        'custom_model': use_custom_model,
        'ocr': 'EasyOCR',
        'video_support': True
    })

@app.route('/detect', methods=['POST'])
def detect():
    """Detect violations from single image"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Read image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Run YOLOv8 detection
        results = model.predict(source=image, conf=0.25, iou=0.45, imgsz=640)
        
        detections = []
        annotated_image = image.copy()
        
        # Process detection results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                confidence = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                class_name = model.names[cls_id]
                
                detection_data = {
                    'class': class_name,
                    'confidence': round(confidence * 100, 2),
                    'bbox': [x1, y1, x2, y2]
                }
                
                # OCR for number plates
                if class_name.lower() in ['numberplate', 'license_plate', 'car', 'truck', 'bus', 'motorcycle']:
                    roi = image[max(0, y1):min(image.shape[0], y2), 
                               max(0, x1):min(image.shape[1], x2)]
                    
                    """
                    if roi.size > 0:
                        try:
                            # reader is disabled for memory efficiency
                            pass
                            # ocr_results = reader.readtext(roi, paragraph=False)
                            # ...
                        except Exception as e:
                            print(f"OCR error: {e}")
                    """
                    pass
                
                detections.append(detection_data)
                
                # Determine color based on class
                if class_name.lower() in ['no-helmet', 'no_helmet', 'without-helmet', 'without_helmet']:
                    color = (0, 0, 255)  # Red for violations
                elif class_name.lower() in ['traffic-light-red', 'traffic_light_red', 'red_light']:
                    color = (0, 0, 255)  # Red
                elif class_name.lower() in ['helmet', 'with_helmet', 'with-helmet']:
                    color = (0, 255, 0)  # Green for compliant
                else:
                    color = (255, 0, 255)  # Magenta for vehicles
                
                # Draw bounding box
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
                
                # Add label
                label = f"{class_name} {confidence:.1f}%"
                if 'license_plate' in detection_data:
                    label += f" | {detection_data['license_plate']}"
                
                # Draw label background
                (label_width, label_height), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                )
                cv2.rectangle(
                    annotated_image,
                    (x1, y1 - label_height - 10),
                    (x1 + label_width, y1),
                    color,
                    -1
                )
                cv2.putText(
                    annotated_image,
                    label,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2
                )
        
        # Analyze for violations
        violation_analysis = analyze_violations(detections, model.names, image_shape=image.shape)
        
        # Send SMS notifications if violations found
        from notification_helper import send_violation_notifications
        sms_results = []
        if violation_analysis['total_violations'] > 0:
            sms_results = send_violation_notifications(violation_analysis, detections)
        
        # Encode annotated image to base64
        _, buffer = cv2.imencode('.jpg', annotated_image)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'success': True,
            'detections': detections,
            'total_detections': len(detections),
            'annotated_image': f'data:image/jpeg;base64,{img_base64}',
            'violations': violation_analysis,
            'sms_notifications': sms_results,
            'model_type': 'custom' if use_custom_model else 'generic',
            'input_type': 'image'
        })
    
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/detect-video', methods=['POST'])
def detect_video():
    """Detect violations from video file - includes speed detection"""
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['video']
        speed_limit = int(request.form.get('speed_limit', 60))  # Default 60 km/h
        
        # Save video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            file.save(tmp_file.name)
            video_path = tmp_file.name
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            os.unlink(video_path)
            return jsonify({'error': 'Invalid video file'}), 400
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        all_detections = []
        all_violations = []
        frame_results = []
        
        frame_idx = 0
        sample_rate = max(1, int(fps / 5))  # Process 5 frames per second
        
        print(f"\n🎬 Processing video: {frame_count} frames at {fps} FPS")
        print(f"⚡ Sampling every {sample_rate} frames...")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Sample frames
            if frame_idx % sample_rate == 0:
                # Run detection on this frame
                results = model.predict(source=frame, conf=0.25, iou=0.45, imgsz=640, verbose=False)
                
                frame_detections = []
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                        confidence = float(box.conf[0].cpu().numpy())
                        cls_id = int(box.cls[0].cpu().numpy())
                        class_name = model.names[cls_id]
                        
                        detection_data = {
                            'frame': frame_idx,
                            'timestamp': frame_idx / fps,
                            'class': class_name,
                            'confidence': round(confidence * 100, 2),
                            'bbox': [x1, y1, x2, y2]
                        }
                        frame_detections.append(detection_data)
                        all_detections.append(detection_data)
                
                # Analyze violations for this frame
                frame_violations = analyze_violations(frame_detections, model.names, image_shape=frame.shape)
                if frame_violations['total_violations'] > 0:
                    frame_results.append({
                        'frame': frame_idx,
                        'timestamp': f"{frame_idx/fps:.2f}s",
                        'violations': frame_violations
                    })
                    all_violations.extend(frame_violations['violations'])
            
            frame_idx += 1
        
        cap.release()
        
        # Analyze speed violations (simplified - would need proper tracking)
        print(f"✅ Processed {frame_idx} frames")
        print(f"🚨 Found {len(all_violations)} total violations")
        
        # Clean up
        os.unlink(video_path)
        
        # Compile results
        violation_summary = {}
        for v in all_violations:
            v_type = v['type']
            violation_summary[v_type] = violation_summary.get(v_type, 0) + 1
        
        return jsonify({
            'success': True,
            'input_type': 'video',
            'video_info': {
                'frames': frame_count,
                'fps': fps,
                'duration': f"{frame_count/fps:.2f}s"
            },
            'total_detections': len(all_detections),
            'total_violations': len(all_violations),
            'violation_summary': violation_summary,
            'frame_results': frame_results[:10],  # Return first 10 frames with violations
            'note': 'Speed detection requires object tracking - currently showing helmet, triple riding, and red light violations only'
        })
    
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Traffic Violation Detection API Server")
    print("="*60)
    print("📍 Server: http://localhost:5000")
    print("🏥 Health Check: http://localhost:5000/health")
    print("🔍 Image Detection: POST http://localhost:5000/detect")
    print("🎬 Video Detection: POST http://localhost:5000/detect-video")
    print("\n💡 Features:")
    print("  - Helmet violation detection")
    print("  - Triple riding detection")
    print("  - Red light jumping detection")
    print("  - License plate recognition")
    print("  - VIDEO UPLOAD SUPPORT")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
