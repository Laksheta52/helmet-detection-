"""
Test script for helmet detection integration
"""
import requests
import cv2
import base64
import json
from pathlib import Path

def test_helmet_detection_api():
    """Test the helmet detection API endpoint"""
    print("="*60)
    print("Testing Helmet Detection API Integration")
    print("="*60)
    
    # API endpoint
    url = "http://localhost:5000/detect"
    
    # Check if backend is running
    try:
        health_response = requests.get("http://localhost:5000/health", timeout=2)
        print(f"\n✓ Backend Status: {health_response.json()}")
    except requests.exceptions.RequestException:
        print("\n❌ Backend server is not running!")
        print("\nPlease start the backend server:")
        print("  cd backend")
        print("  python app.py")
        return
    
    # Test with sample image from dataset
    helmet_dataset_images = Path("helmet_detection/val/images")
    
    if helmet_dataset_images.exists():
        images = list(helmet_dataset_images.glob("*.png"))
        if images:
            test_image = str(images[0])
            print(f"\n📷 Testing with image: {test_image}")
            
            # Send request
            with open(test_image, 'rb') as f:
                files = {'image': f}
                response = requests.post(url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n✓  Detection successful!")
                print(f"   Total detections: {result.get('total_detections', 0)}")
                print(f"   Model type: {result.get('model_type', 'unknown')}")
                
                if 'detections' in result:
                    print(f"\n🎯 Detections:")
                    for det in result['detections']:
                        print(f"   - {det['class']}: {det['confidence']}%")
                
                if 'violations' in result:
                    violations = result['violations']
                    print(f"\n🚨 Violations: {violations.get('total_violations', 0)}")
                    if violations.get('total_violations', 0) > 0:
                        for v in violations.get('violations', []):
                            print(f"   - {v['type']}: {v.get('description', '')}")
                
                print("\n✅ Integration test passed!")
            else:
                print(f"\n❌ Error: {response.status_code}")
                print(response.text)
        else:
            print("\n⚠ No images found in validation set")
    else:
        print(f"\n⚠ Validation dataset not found at: {helmet_dataset_images}")
        print("   Please run prepare_helmet_dataset.py first")

def test_local_inference():
    """Test helmet detection locally without API"""
    print("\n" + "="*60)
    print("Testing Local Helmet Detection")
    print("="*60)
    
    try:
        from helmet_detector import HelmetDetector
        
        detector = HelmetDetector('backend/best.pt')
        
        # Test with validation image
        helmet_dataset_images = Path("helmet_detection/val/images")
        if helmet_dataset_images.exists():
            images = list(helmet_dataset_images.glob("*.png"))
            if images:
                test_image = str(images[0])
                print(f"\n📷 Testing with: {test_image}")
                
                img = cv2.imread(test_image)
                if img is not None:
                    detections = detector.detect(img)
                    print(f"\n✓ Found {len(detections)} detections:")
                    
                    for det in detections:
                        print(f"   - {det['class']}: {det['confidence']}% {'🚨 VIOLATION' if det['is_violation'] else '✓'}")
                    
                    # Save annotated image
                    annotated = detector.annotate_image(img, detections)
                    output_path = "helmet_detection_test.jpg"
                    cv2.imwrite(output_path, annotated)
                    print(f"\n✅ Saved annotated result to: {output_path}")
                else:
                    print("❌ Error loading image")
        else:
            print(f"⚠ Validation dataset not found")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🧪 Helmet Detection Integration Test Suite\n")
    
    # Test local inference first
    test_local_inference()
    
    # Test API endpoint
    test_helmet_detection_api()
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)
