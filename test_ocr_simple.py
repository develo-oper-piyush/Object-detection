"""
Simple OCR test to verify EasyOCR can read license plates
"""
import cv2
import numpy as np

try:
    import easyocr
    print("✓ EasyOCR imported successfully")
except ImportError:
    print("✗ EasyOCR not found. Install with: pip install easyocr")
    exit(1)

# Initialize reader
print("\nLoading EasyOCR model...")
reader = easyocr.Reader(['en'], gpu=False, verbose=False)
print("✓ EasyOCR loaded!")

# Create a test image with a license plate
print("\nCreating test license plate image...")
test_img = np.ones((200, 600, 3), dtype=np.uint8) * 255  # White background

# Draw a plate-like rectangle
cv2.rectangle(test_img, (100, 50), (500, 150), (0, 0, 0), 2)
cv2.rectangle(test_img, (100, 50), (500, 150), (255, 200, 0), -1)  # Blue background

# Add text
cv2.putText(test_img, "ABC 1234", (150, 110), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5)

# Save test image
cv2.imwrite("test_plate.jpg", test_img)
print("✓ Test image created: test_plate.jpg")

# Try to read it
print("\nAttempting to read license plate...")
results = reader.readtext(test_img, detail=1)

if results:
    print(f"✓ OCR Results ({len(results)} detections):")
    for i, (bbox, text, confidence) in enumerate(results, 1):
        print(f"  {i}. Text: '{text}' | Confidence: {confidence:.2f}")
        cleaned = ''.join(c for c in text if c.isalnum())
        print(f"     Cleaned: '{cleaned}'")
else:
    print("✗ No text detected!")

print("\n" + "="*60)
print("If you see 'ABC1234' or similar above, OCR is working!")
print("If not, there may be an issue with the EasyOCR installation.")
print("="*60)

# Now test with a darker image (more realistic)
print("\n\nTesting with realistic dark plate...")
test_img2 = np.ones((100, 300, 3), dtype=np.uint8) * 50  # Dark background
cv2.rectangle(test_img2, (20, 20), (280, 80), (255, 255, 255), -1)  # White plate
cv2.putText(test_img2, "XYZ789", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

cv2.imwrite("test_plate2.jpg", test_img2)
results2 = reader.readtext(test_img2, detail=1)

if results2:
    print(f"✓ Realistic plate OCR ({len(results2)} detections):")
    for i, (bbox, text, confidence) in enumerate(results2, 1):
        cleaned = ''.join(c for c in text if c.isalnum())
        print(f"  {i}. Text: '{cleaned}' | Confidence: {confidence:.2f}")
else:
    print("✗ No text detected on realistic plate")

print("\n✅ OCR Test Complete!")
print("\nNOTE: If OCR works here but not in your video:")
print("  1. License plates in video may be too small")
print("  2. Plates may be at an angle")
print("  3. Motion blur or poor lighting")
print("  4. Try testing with a video that has clear, visible plates")
