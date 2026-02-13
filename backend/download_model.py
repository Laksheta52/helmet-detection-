"""
Download Pre-trained Helmet Detection Model
Downloads model from Hugging Face: sharathhhhh/safetyHelmet-detection-yolov8
"""

import os
import urllib.request
import sys

def download_model():
    """Download pre-trained helmet detection model from Hugging Face"""
    
    print("="*60)
    print("🚀 Downloading Pre-trained Helmet Detection Model")
    print("="*60)
    print("\n📦 Source: Hugging Face")
    print("🤖 Model: sharathhhhh/safetyHelmet-detection-yolov8")
    print("\n🎯 Classes:")
    print("  - with_helmet (person wearing helmet)")
    print("  - without_helmet (helmet violation)")
    print("\n" + "="*60 + "\n")
    
    # Hugging Face model URL
    model_url = "https://huggingface.co/sharathhhhh/safetyHelmet-detection-yolov8/resolve/main/best.pt"
    output_path = "best.pt"
    
    # Check if model already exists
    if os.path.exists(output_path):
        print(f"⚠️  Model file '{output_path}' already exists!")
        response = input("Do you want to re-download? (y/n): ")
        if response.lower() != 'y':
            print("✅ Using existing model file.")
            return True
        print("\n🔄 Re-downloading model...")
    
    try:
        print(f"📥 Downloading from Hugging Face...")
        print(f"🔗 URL: {model_url}")
        print(f"💾 Saving to: {os.path.abspath(output_path)}")
        print("\n⏳ This may take a few minutes (file size: ~12-25 MB)...\n")
        
        def progress_hook(count, block_size, total_size):
            """Show download progress"""
            percent = int(count * block_size * 100 / total_size)
            mb_downloaded = (count * block_size) / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            
            # Update progress bar
            bar_length = 40
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            sys.stdout.write(f'\r[{bar}] {percent}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)')
            sys.stdout.flush()
        
        # Download with progress
        urllib.request.urlretrieve(model_url, output_path, reporthook=progress_hook)
        
        print("\n\n" + "="*60)
        print("✅ MODEL DOWNLOADED SUCCESSFULLY!")
        print("="*60)
        
        # Verify file
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n📊 Model Details:")
        print(f"  File: {os.path.abspath(output_path)}")
        print(f"  Size: {file_size:.1f} MB")
        
        print("\n🎯 Model Capabilities:")
        print("  ✅ Detects: Helmet violations (with/without helmet)")
        print("  ✅ Format: YOLOv8")
        print("  ✅ Input: 640x640 images")
        print("  ✅ Ready to use!")
        
        print("\n🚀 Next Steps:")
        print("  1. Model is already in the correct location (backend\\)")
        print("  2. Restart your backend server:")
        print("     cd backend")
        print("     .\\start.bat")
        print("  3. Open http://localhost:3000")
        print("  4. Upload traffic images and see violations detected!")
        
        print("\n" + "="*60)
        
        return True
        
    except Exception as e:
        print(f"\n\n❌ Error downloading model: {str(e)}")
        print("\n💡 Alternative Options:")
        print("  1. Manual download:")
        print(f"     Visit: https://huggingface.co/sharathhhhh/safetyHelmet-detection-yolov8")
        print("     Download 'best.pt' and place in backend folder")
        print("\n  2. Train your own:")
        print("     Use AUTOMATED_Training.ipynb in Google Colab")
        return False

if __name__ == "__main__":
    print("\n")
    success = download_model()
    
    if success:
        print("\n✨ Your traffic violation detection system is ready!")
        print("🎉 Run 'start-all.bat' to start the application!\n")
    else:
        print("\n⚠️  Please try alternative download methods.\n")
    
    input("Press Enter to exit...")
