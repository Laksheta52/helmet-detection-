"""
Helmet Detection Inference Script
Handles helmet detection using the trained YOLOv8 model
"""
from ultralytics import YOLO
import cv2
import numpy as np

class HelmetDetector:
    def __init__(self, model_path='best.pt'):
        """Initialize the helmet detector with trained model"""
        self.model = YOLO(model_path)
        print(f"✓ Loaded helmet detection model: {model_path}")
        print(f"Classes: {self.model.names}")
    
    def detect(self, image, conf=0.25):
        """
        Detect helmets in an image
        
        Args:
            image: numpy array (BGR format)
            conf: confidence threshold (default 0.25)
        
        Returns:
            List of detections with class, confidence, and bounding box
        """
        results = self.model.predict(source=image, conf=conf, iou=0.45, imgsz=640, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                confidence = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                class_name = self.model.names[cls_id]
                
                detections.append({
                    'class': class_name,
                    'confidence': round(confidence * 100, 2),
                    'bbox': [x1, y1, x2, y2],
                    'is_violation': class_name.lower() == 'without_helmet'
                })
        
        return detections
    
    def annotate_image(self, image, detections):
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: numpy array (BGR format)
            detections: list of detection dictionaries
        
        Returns:
            Annotated image
        """
        annotated = image.copy()
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            class_name = det['class']
            confidence = det['confidence']
            
            # Color based on class
            if class_name.lower() == 'without_helmet':
                color = (0, 0, 255)  # Red for violations
            else:
                color = (0, 255, 0)  # Green for with helmet
            
            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label = f"{class_name} {confidence:.1f}%"
            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(annotated, (x1, y1 - label_h - 10), (x1 + label_w, y1), color, -1)
            cv2.putText(annotated, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return annotated

if __name__ == "__main__":
    # Test the detector
    import sys
    
    if len(sys.argv) > 1:
        detector = HelmetDetector()
        img = cv2.imread(sys.argv[1])
        if img is not None:
            detections = detector.detect(img)
            print(f"\nDetections: {len(detections)}")
            for det in detections:
                print(f"  - {det['class']}: {det['confidence']}%")
            
            annotated = detector.annotate_image(img, detections)
            cv2.imwrite('helmet_detection_result.jpg', annotated)
            print("\nSaved annotated image to helmet_detection_result.jpg")
        else:
            print(f"Error loading image: {sys.argv[1]}")
    else:
        print("Usage: python helmet_detector.py <image_path>")
