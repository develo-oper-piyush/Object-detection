"""
Configuration File for Vehicle Detection System
Modify these settings to customize the system behavior
"""

# ============================================================================
# DETECTION SETTINGS
# ============================================================================

# YOLO Model Selection
# Options: "yolov8n.pt" (fastest), "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt" (most accurate)
YOLO_MODEL = "yolov8n.pt"

# Detection Confidence Threshold
# Lower = more detections (may include false positives)
# Higher = fewer detections (more accurate)
CONFIDENCE_THRESHOLD = 0.25

# Detection Interval
# Process every Nth frame (1 = every frame, 2 = every other frame, etc.)
# Higher values = faster processing but may miss detections
DETECTION_INTERVAL = 1

# ============================================================================
# VEHICLE PRIORITY CLASSIFICATION
# ============================================================================

# You can customize which vehicles belong to which priority level
# Format: 'vehicle_type': 'PRIORITY_LEVEL'

VEHICLE_PRIORITY = {
    # HIGH PRIORITY - Emergency Vehicles
    'ambulance': 'HIGH',
    'fire truck': 'HIGH',
    'police': 'HIGH',
    'police car': 'HIGH',
    'emergency': 'HIGH',
    
    # MEDIUM PRIORITY - Commercial Vehicles
    'bus': 'MEDIUM',
    'truck': 'MEDIUM',
    'semi': 'MEDIUM',
    'lorry': 'MEDIUM',
    'van': 'MEDIUM',
    
    # LOW PRIORITY - Personal Vehicles
    'car': 'LOW',
    'motorcycle': 'LOW',
    'bicycle': 'LOW',
    'motorbike': 'LOW',
    'scooter': 'LOW',
}

# ============================================================================
# LED CONTROL SETTINGS
# ============================================================================

# LED Colors for each priority level
LED_COLORS = {
    'HIGH': 'red',      # Red LED for high priority
    'MEDIUM': 'yellow', # Yellow LED for medium priority
    'LOW': 'green',     # Green LED for low priority
    'NONE': 'off'       # All LEDs off
}

# LED Control Enabled/Disabled
# Set to False to disable LED control entirely
LED_CONTROL_ENABLED = True

# LED HTTP Request Timeout (seconds)
LED_REQUEST_TIMEOUT = 1

# ============================================================================
# ESP32-CAM SETTINGS
# ============================================================================

# Default stream path
DEFAULT_STREAM_PATH = "/stream"

# Connection timeout for stream (seconds)
STREAM_TIMEOUT = 5

# Retry attempts for stream connection
STREAM_RETRY_ATTEMPTS = 3

# ============================================================================
# VIDEO PROCESSING SETTINGS
# ============================================================================

# Video loop on end
# If True, video will restart from beginning when it ends
VIDEO_LOOP_ENABLED = True

# Video playback speed
# 1.0 = normal speed, 0.5 = half speed, 2.0 = double speed
VIDEO_PLAYBACK_SPEED = 1.0

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================

# Window name
WINDOW_TITLE = "ESP32-CAM Vehicle Detection & Priority Classification"

# Display resolution
# Set to None for original resolution, or (width, height) to resize
DISPLAY_RESOLUTION = None  # Example: (1280, 720)

# Bounding box thickness
BBOX_THICKNESS = 2

# Text font size
TEXT_FONT_SCALE = 0.6
TEXT_THICKNESS = 2

# Colors for priority levels (BGR format)
PRIORITY_COLORS = {
    'HIGH': (0, 0, 255),      # Red
    'MEDIUM': (0, 165, 255),  # Orange/Yellow
    'LOW': (0, 255, 0),       # Green
}

# Display current priority status
SHOW_PRIORITY_STATUS = True

# Status text position (x, y)
STATUS_TEXT_POSITION = (10, 30)

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Maximum log entries in memory
# Older entries will be removed when limit is reached
MAX_LOG_ENTRIES = 10000

# Log to console
CONSOLE_LOGGING_ENABLED = True

# Log detection details
LOG_DETECTION_DETAILS = False  # Set to True for verbose logging

# ============================================================================
# EXCEL EXPORT SETTINGS
# ============================================================================

# Excel filename prefix
EXCEL_FILENAME_PREFIX = "vehicle_detections"

# Excel sheet name
EXCEL_SHEET_NAME = "Vehicle Detections"

# Include header row
EXCEL_INCLUDE_HEADER = True

# Export format
# Options: "xlsx" (default), "csv"
EXPORT_FORMAT = "xlsx"

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# GPU Acceleration
# Set to True if you have CUDA-enabled GPU
USE_GPU = False

# Number of worker threads for detection
# Set to 1 for single-threaded, higher for parallel processing
WORKER_THREADS = 1

# Frame buffer size
FRAME_BUFFER_SIZE = 1

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Enable debug mode
DEBUG_MODE = False

# Show FPS counter
SHOW_FPS = False

# Save detection images
SAVE_DETECTION_IMAGES = False
DETECTION_IMAGES_DIR = "detections"

# Enable audio alerts
AUDIO_ALERTS_ENABLED = False

# Alert sound for high priority
HIGH_PRIORITY_SOUND = "alert.wav"  # Path to audio file

# ============================================================================
# CUSTOM VEHICLE KEYWORDS
# ============================================================================

# Additional keywords to detect in labels
# These will be checked in addition to the standard YOLO labels
CUSTOM_VEHICLE_KEYWORDS = {
    'emergency': 'HIGH',
    'patrol': 'HIGH',
    'rescue': 'HIGH',
    'delivery': 'MEDIUM',
    'taxi': 'LOW',
    'suv': 'LOW',
    'sedan': 'LOW',
}

# ============================================================================
# GPIO PIN CONFIGURATION (for reference - edit in Arduino code)
# ============================================================================

# These pins are defined in the Arduino sketch
# Listed here for reference only
GPIO_LED_RED = 12      # High priority
GPIO_LED_YELLOW = 13   # Medium priority
GPIO_LED_GREEN = 15    # Low priority

# ============================================================================
# NOTES
# ============================================================================

"""
Usage:
1. Modify the settings above as needed
2. Save this file
3. Import in new.py: from config import *
4. Use the configuration variables in your code

Example:
    model = YOLO(YOLO_MODEL)
    if CONFIDENCE_THRESHOLD:
        results = model(frame, conf=CONFIDENCE_THRESHOLD)
"""
