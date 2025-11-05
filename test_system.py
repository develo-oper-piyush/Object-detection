"""
Test Script for Vehicle Detection System
This script helps verify that the system is working correctly
"""

import sys
import os

def check_dependencies():
    """Check if all required Python packages are installed"""
    print("Checking dependencies...")
    required_packages = {
        'cv2': 'opencv-python',
        'ultralytics': 'ultralytics',
        'openpyxl': 'openpyxl',
        'requests': 'requests',
        'tkinter': 'built-in'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            if module == 'tkinter':
                import tkinter
            else:
                __import__(module)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join([p for p in missing if p != 'built-in']))
        return False
    else:
        print("\n✓ All dependencies are installed!")
        return True

def test_yolo_model():
    """Test if YOLO model can be loaded"""
    print("\nTesting YOLO model...")
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")
        print("✓ YOLO model loaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error loading YOLO model: {e}")
        return False

def check_video_file(video_path):
    """Check if a video file exists and can be opened"""
    import cv2
    
    if not os.path.exists(video_path):
        print(f"✗ Video file not found: {video_path}")
        return False
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"✗ Cannot open video file: {video_path}")
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    
    print(f"✓ Video file OK:")
    print(f"  - Resolution: {width}x{height}")
    print(f"  - FPS: {fps}")
    print(f"  - Frames: {frame_count}")
    return True

def main():
    print("=" * 60)
    print("Vehicle Detection System - Test Script")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return False
    
    # Test YOLO model
    if not test_yolo_model():
        print("\n❌ YOLO model test failed")
        return False
    
    # Check for video files in current directory
    print("\nChecking for video files in current directory...")
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv']
    video_files = [f for f in os.listdir('.') if any(f.lower().endswith(ext) for ext in video_extensions)]
    
    if video_files:
        print(f"Found {len(video_files)} video file(s):")
        for vf in video_files:
            print(f"  - {vf}")
            check_video_file(vf)
    else:
        print("No video files found in current directory")
        print("You can test with a video file by running:")
        print("  python new.py --video your_video.mp4")
    
    print("\n" + "=" * 60)
    print("✓ System is ready!")
    print("=" * 60)
    print("\nUsage:")
    print("  With ESP32-CAM: python new.py --ip 192.168.1.50")
    print("  With video file: python new.py --video traffic_video.mp4")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
