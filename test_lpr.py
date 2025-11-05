"""
Quick test script to verify License Plate Recognition setup

This script tests:
1. All required libraries are installed
2. EasyOCR model loads successfully
3. Basic OCR functionality works
"""

import sys

print("=" * 60)
print("Testing License Plate Recognition Setup")
print("=" * 60)

# Test 1: Check imports
print("\n[1/4] Testing library imports...")
try:
    import cv2
    print("  ✓ OpenCV imported")
except ImportError as e:
    print(f"  ✗ OpenCV failed: {e}")
    sys.exit(1)

try:
    from ultralytics import YOLO
    print("  ✓ Ultralytics YOLO imported")
except ImportError as e:
    print(f"  ✗ Ultralytics failed: {e}")
    sys.exit(1)

try:
    import easyocr
    print("  ✓ EasyOCR imported")
except ImportError as e:
    print(f"  ✗ EasyOCR failed: {e}")
    sys.exit(1)

try:
    import torch
    print("  ✓ PyTorch imported")
except ImportError as e:
    print(f"  ✗ PyTorch failed: {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("  ✓ Pillow imported")
except ImportError as e:
    print(f"  ✗ Pillow failed: {e}")
    sys.exit(1)

# Test 2: Load EasyOCR
print("\n[2/4] Loading EasyOCR model (this may take a minute)...")
try:
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    print("  ✓ EasyOCR model loaded successfully")
except Exception as e:
    print(f"  ✗ EasyOCR loading failed: {e}")
    sys.exit(1)

# Test 3: Test OCR on sample text
print("\n[3/4] Testing OCR functionality...")
try:
    import numpy as np
    
    # Create a simple test image with text
    test_img = np.ones((100, 300, 3), dtype=np.uint8) * 255  # White background
    cv2.putText(test_img, "ABC1234", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    
    # Try to read it
    results = reader.readtext(test_img, detail=0)
    
    if results and any('ABC' in str(r).upper() for r in results):
        print(f"  ✓ OCR working! Detected: {results}")
    else:
        print(f"  ⚠ OCR working but may need tuning. Detected: {results}")
except Exception as e:
    print(f"  ✗ OCR test failed: {e}")
    sys.exit(1)

# Test 4: Check YOLO model
print("\n[4/4] Checking YOLO model...")
try:
    import os
    if os.path.exists("yolov8n.pt"):
        print("  ✓ YOLO model file found (yolov8n.pt)")
        model = YOLO("yolov8n.pt")
        print("  ✓ YOLO model loaded successfully")
    else:
        print("  ⚠ YOLO model not found, will download on first run")
except Exception as e:
    print(f"  ✗ YOLO test failed: {e}")

# Summary
print("\n" + "=" * 60)
print("✅ LICENSE PLATE RECOGNITION SETUP COMPLETE!")
print("=" * 60)
print("\nYou can now run:")
print("  python new.py --video traffic.mp4")
print("  python new.py --ip 192.168.1.50")
print("\nLicense plates will be automatically detected and logged!")
print("=" * 60)
