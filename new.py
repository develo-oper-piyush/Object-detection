"""
ESP32-CAM Object Detection System with Multiple Modes

This script provides THREE detection modes:
  1. VEHICLE MODE (default): Vehicle detection with priority classification
  2. GENERAL MODE: Detect 80+ everyday objects (COCO dataset)
  3. PEDESTRIAN MODE: Add pedestrian detection to vehicle mode

Usage:
  - Upload the provided Arduino sketch to your ESP32-CAM (see README).
  - Make sure the ESP32-CAM is on your Wi-Fi and note its IP address.
  - Install Python requirements: pip install -r requirements.txt
  
  VEHICLE MODE (default):
    python new.py --ip 192.168.x.y
    python new.py --video path/to/video.mp4
  
  GENERAL OBJECT DETECTION MODE:
    python new.py --video path/to/video.mp4 --general-objects
    python new.py --ip 192.168.x.y --general-objects
  
  WITH PEDESTRIAN DETECTION:
    python new.py --video path/to/video.mp4 --pedestrians
    python new.py --video path/to/video.mp4 --general-objects --pedestrians

Features:
  - VEHICLE MODE: Detects cars, trucks, buses, motorcycles, bicycles with priority
  - GENERAL MODE: Detects 80+ objects (person, dog, cat, chair, laptop, etc.)
  - License Plate Recognition (Vehicle mode only)
  - ESP32-CAM LED control based on priority
  - Excel export with detection logs
  - Real-time FPS and detection stats

Notes:
  - The script requires internet the first time to download YOLO weights.
  - LED colors: RED = High Priority, YELLOW = Medium Priority, GREEN = Low Priority
"""
import argparse
import threading
import time
from datetime import datetime
from collections import deque
import sys
import os

import cv2
import requests

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None

try:
    import tkinter as tk
    from tkinter import messagebox
except Exception:
    tk = None

try:
    import openpyxl
    from openpyxl import Workbook
except Exception:
    openpyxl = None

try:
    import easyocr
except Exception:
    easyocr = None


# COCO Dataset - 80 Object Classes that YOLO can detect
COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


# Vehicle priority classification
VEHICLE_PRIORITY = {
    # High Priority - Emergency Vehicles
    'ambulance': 'HIGH',
    'fire truck': 'HIGH',
    'police': 'HIGH',
    
    # Medium Priority - Commercial Vehicles
    'bus': 'MEDIUM',
    'truck': 'MEDIUM',
    
    # Low Priority - Personal Vehicles
    'car': 'LOW',
    'motorcycle': 'LOW',
    'bicycle': 'LOW',
    'motorbike': 'LOW'
}

# LED control colors for ESP32
LED_COLORS = {
    'HIGH': 'red',      # Red LED for high priority
    'MEDIUM': 'yellow', # Yellow LED for medium priority
    'LOW': 'green',     # Green LED for low priority
    'NONE': 'off'       # All LEDs off
}


class ESP32CamDetector:
    def __init__(self, esp_ip=None, stream_path="/stream", video_path=None, process_scale=1.0, 
                 detect_pedestrians=False, general_mode=False):
        self.esp_ip = esp_ip
        self.video_path = video_path
        self.use_video = video_path is not None
        self.process_scale = process_scale  # Scale factor for processing (0.5 = half size for 4x speed)
        self.detect_pedestrians = detect_pedestrians  # Enable pedestrian detection
        self.general_mode = general_mode  # Enable general object detection (80+ classes)
        
        if esp_ip and esp_ip.startswith("http"):
            self.stream_url = esp_ip
        elif esp_ip:
            self.stream_url = f"http://{esp_ip}{stream_path}"
        else:
            self.stream_url = None

        self.cap = None
        self.model = None
        self.ocr_reader = None
        self.running = False
        self.log = deque()  # store (timestamp_iso, label, priority, license_plate, pedestrian_count)
        self.frame = None
        self.current_priority = 'NONE'  # Track highest priority vehicle detected
        self.plate_cache = {}  # Cache to avoid reading same plate multiple times
        self.plate_cache_timeout = 3  # seconds
        self.last_annotated = None  # Store last annotated frame to prevent blinking
        self.max_vehicles = 5  # Only track 5 nearest vehicles
        self.pedestrian_count = 0  # Track pedestrians in current frame
        self.object_counts = {}  # Track counts of different objects in general mode

    def load_model(self):
        if YOLO is None:
            raise RuntimeError("Ultralytics YOLO not available. Install with: pip install ultralytics")
        # use small model for speed
        self.model = YOLO("yolov8n.pt")
        
        # Initialize EasyOCR for license plate recognition
        if easyocr is not None:
            print("Loading EasyOCR for license plate recognition (this may take a minute)...")
            try:
                self.ocr_reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if CUDA available
                print("EasyOCR loaded successfully!")
            except Exception as e:
                print(f"Warning: Could not load EasyOCR: {e}")
                print("License plate recognition will be disabled.")
                self.ocr_reader = None
        else:
            print("EasyOCR not installed. License plate recognition disabled.")
            print("Install with: pip install easyocr")

    def start_capture(self):
        if self.use_video:
            if not os.path.exists(self.video_path):
                raise RuntimeError(f"Video file not found: {self.video_path}")
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open video file at {self.video_path}")
        else:
            if not self.stream_url:
                raise RuntimeError("No stream URL or video file provided")
            
            print(f"Connecting to stream: {self.stream_url}")
            
            # Try to open the stream
            self.cap = cv2.VideoCapture(self.stream_url)
            
            # For IP camera apps, may need to set buffer size
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open stream at {self.stream_url}")
            
            print("Successfully connected to IP camera stream!")

    def classify_vehicle_priority(self, label):
        """Classify vehicle by priority based on its type"""
        label_lower = label.lower()
        
        # Check for emergency vehicles (high priority)
        if any(keyword in label_lower for keyword in ['ambulance', 'fire', 'police']):
            return 'HIGH'
        
        # Check if it's a known vehicle type
        for vehicle_type, priority in VEHICLE_PRIORITY.items():
            if vehicle_type in label_lower:
                return priority
        
        # Default: not a vehicle or unknown
        return None
    
    def preprocess_plate_roi(self, plate_roi):
        """Preprocess image region for better OCR accuracy"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
            
            # Apply bilateral filter to reduce noise
            denoised = cv2.bilateralFilter(gray, 11, 17, 17)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Resize if too small (minimum height 50px for better OCR)
            height, width = thresh.shape
            if height < 50:
                scale = 50 / height
                new_width = int(width * scale)
                thresh = cv2.resize(thresh, (new_width, 50), interpolation=cv2.INTER_CUBIC)
            
            return thresh
        except Exception as e:
            return plate_roi
    
    def detect_license_plate(self, frame, x1, y1, x2, y2, vehicle_id):
        """
        Detect and read license plate from vehicle region
        
        Args:
            frame: Full video frame
            x1, y1, x2, y2: Bounding box coordinates of detected vehicle
            vehicle_id: Unique identifier for caching purposes
            
        Returns:
            License plate text or None
        """
        if self.ocr_reader is None:
            return None
        
        # Check cache first (avoid re-reading same plate)
        current_time = time.time()
        if vehicle_id in self.plate_cache:
            cached_plate, cached_time = self.plate_cache[vehicle_id]
            if current_time - cached_time < self.plate_cache_timeout:
                return cached_plate
        
        try:
            # Extract vehicle region with some padding
            height, width = frame.shape[:2]
            pad = 10
            y1_pad = max(0, y1 - pad)
            y2_pad = min(height, y2 + pad)
            x1_pad = max(0, x1 - pad)
            x2_pad = min(width, x2 + pad)
            
            vehicle_roi = frame[y1_pad:y2_pad, x1_pad:x2_pad]
            
            if vehicle_roi.size == 0 or vehicle_roi.shape[0] < 20 or vehicle_roi.shape[1] < 20:
                return None
            
            # Focus on lower 40% of vehicle (where plates typically are)
            roi_height = vehicle_roi.shape[0]
            lower_region = vehicle_roi[int(roi_height * 0.6):, :]
            
            if lower_region.size == 0:
                lower_region = vehicle_roi
            
            # Preprocess the image
            processed = self.preprocess_plate_roi(lower_region)
            
            # Perform OCR
            results = self.ocr_reader.readtext(processed, detail=1, paragraph=False)
            
            if not results:
                return None
            
            # Filter and clean results
            best_plate = None
            best_confidence = 0
            
            for (bbox, text, confidence) in results:
                # Lower confidence threshold and more lenient validation
                if confidence > 0.3:  # Lowered from 0.4
                    # Clean the text (remove spaces, special chars except hyphens)
                    cleaned_text = ''.join(c for c in text if c.isalnum() or c == '-')
                    
                    # More lenient: 3-12 chars, can be all numbers or all letters
                    if 3 <= len(cleaned_text) <= 12:
                        # Accept if it has numbers OR letters (not necessarily both)
                        has_letter = any(c.isalpha() for c in cleaned_text)
                        has_number = any(c.isdigit() for c in cleaned_text)
                        
                        # Accept any text with letters or numbers
                        if (has_letter or has_number) and confidence > best_confidence:
                            best_plate = cleaned_text.upper()
                            best_confidence = confidence
                            # Debug output
                            print(f"🔍 Detected plate: {best_plate} (confidence: {confidence:.2f})")
            
            # Cache the result
            if best_plate:
                self.plate_cache[vehicle_id] = (best_plate, current_time)
            
            return best_plate
            
        except Exception as e:
            # Print errors for debugging
            print(f"⚠️ OCR error: {e}")
            return None
    
    def clean_old_cache(self):
        """Remove old entries from plate cache"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.plate_cache.items()
            if current_time - timestamp > self.plate_cache_timeout
        ]
        for key in expired_keys:
            del self.plate_cache[key]
    
    def send_led_command(self, priority):
        """Send LED control command to ESP32"""
        if self.use_video or not self.esp_ip:
            return  # Skip LED control for video files
        
        try:
            color = LED_COLORS.get(priority, 'off')
            url = f"http://{self.esp_ip}/led?color={color}"
            requests.get(url, timeout=1)
        except Exception as e:
            # Don't crash on LED control errors
            pass

    def run(self):
        self.running = True
        if self.model is None:
            self.load_model()
        if self.cap is None:
            self.start_capture()

        # Determine mode
        if self.general_mode:
            mode_str = "GENERAL OBJECT DETECTION (80+ classes)"
        else:
            mode_str = "VEHICLE DETECTION with priority classification"
        
        source_type = "video file" if self.use_video else "ESP32 stream"
        print(f"Starting {mode_str} from {source_type}.")
        print(f"Press 'q' in the video window to quit, 'e' to export data.")
        
        frame_count = 0
        detection_interval = 3  # Process every 3rd frame for better performance
        ocr_interval = 15  # Only run OCR every 15th frame (OCR is slow!)
        
        # Calculate proper wait time for video playback
        if self.use_video:
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            if fps == 0 or fps > 120:  # Invalid FPS
                fps = 30  # Default to 30 FPS
            wait_time = int(1000 / fps)  # milliseconds per frame
        else:
            wait_time = 1  # For live stream, process as fast as possible
        
        print(f"Video FPS: {fps if self.use_video else 'N/A'}, Wait time: {wait_time}ms")
        print(f"Tracking max {self.max_vehicles} nearest vehicles for better performance")
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                if self.use_video:
                    # Video ended, restart or quit
                    print("Video ended. Restarting...")
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    # Stream issue, retry
                    time.sleep(0.1)
                    continue
            
            self.frame = frame
            frame_count += 1
            
            # Resize frame for faster processing if scale < 1.0
            if self.process_scale < 1.0:
                process_frame = cv2.resize(frame, None, fx=self.process_scale, fy=self.process_scale, 
                                          interpolation=cv2.INTER_LINEAR)
                scale_factor = 1.0 / self.process_scale
            else:
                process_frame = frame
                scale_factor = 1.0

            # Detect vehicles on this frame
            if frame_count % detection_interval == 0:
                # Clean old cache entries periodically
                if frame_count % 30 == 0:
                    self.clean_old_cache()
                
                try:
                    results = self.model(process_frame)
                except Exception as e:
                    print("Detection error:", e)
                    time.sleep(0.5)
                    continue

                annotated = frame.copy()
                frame_priorities = []  # Track all priorities detected in this frame
                
                # Determine if we should run OCR this frame (only every Nth frame)
                run_ocr = (frame_count % ocr_interval == 0)
                
                # Collect all vehicle detections first
                vehicle_detections = []
                pedestrian_detections = []
                general_detections = []  # For general object detection mode
                
                # Process detection results
                for r in results:
                    boxes = r.boxes
                    if boxes is None:
                        continue
                    for idx, box in enumerate(boxes):
                        xyxy = box.xyxy[0].cpu().numpy() if hasattr(box.xyxy[0], 'cpu') else box.xyxy[0].numpy()
                        # Scale coordinates back to original frame size
                        x1, y1, x2, y2 = map(int, xyxy[:4] * scale_factor)
                        conf = float(box.conf[0]) if hasattr(box, 'conf') and len(box.conf) else 0.0
                        cls = int(box.cls[0]) if hasattr(box, 'cls') and len(box.cls) else None
                        name = r.names[cls] if (cls is not None and r.names is not None and cls in r.names) else str(cls)

                        # GENERAL OBJECT DETECTION MODE
                        if self.general_mode:
                            # Detect ALL objects from COCO dataset (80+ classes)
                            frame_height = frame.shape[0]
                            distance = frame_height - y2
                            
                            general_detections.append({
                                'bbox': (x1, y1, x2, y2),
                                'conf': conf,
                                'name': name,
                                'distance': distance,
                                'cls': cls
                            })
                            continue  # Skip vehicle-specific logic in general mode
                        
                        # VEHICLE MODE (default behavior)
                        # Check if it's a pedestrian (person detection)
                        if self.detect_pedestrians and name.lower() == 'person':
                            # Calculate distance from bottom center
                            frame_height = frame.shape[0]
                            distance = frame_height - y2
                            
                            pedestrian_detections.append({
                                'bbox': (x1, y1, x2, y2),
                                'conf': conf,
                                'distance': distance
                            })
                        
                        # Classify vehicle priority
                        priority = self.classify_vehicle_priority(name)
                        
                        if priority:  # Only process if it's a vehicle
                            # Calculate distance from bottom center (nearer = larger y2 value)
                            frame_height = frame.shape[0]
                            distance = frame_height - y2  # Lower distance = closer to camera
                            
                            vehicle_detections.append({
                                'bbox': (x1, y1, x2, y2),
                                'conf': conf,
                                'name': name,
                                'priority': priority,
                                'distance': distance
                            })
                
                # Sort by distance and keep only the 5 nearest vehicles
                vehicle_detections.sort(key=lambda v: v['distance'])
                nearest_vehicles = vehicle_detections[:self.max_vehicles]
                
                # Update pedestrian count
                self.pedestrian_count = len(pedestrian_detections)
                
                # =============== GENERAL OBJECT DETECTION MODE ===============
                if self.general_mode:
                    # Sort by confidence for better display
                    general_detections.sort(key=lambda d: d['conf'], reverse=True)
                    
                    # Update object counts
                    self.object_counts.clear()
                    for obj in general_detections:
                        obj_name = obj['name']
                        self.object_counts[obj_name] = self.object_counts.get(obj_name, 0) + 1
                    
                    # Draw all detected objects
                    color_map = {}  # Cache colors for each class
                    import random
                    random.seed(42)  # Consistent colors
                    
                    for obj in general_detections:
                        x1, y1, x2, y2 = obj['bbox']
                        conf = obj['conf']
                        name = obj['name']
                        cls = obj['cls']
                        
                        # Generate consistent color for each object class
                        if cls not in color_map:
                            color_map[cls] = (
                                random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)
                            )
                        color = color_map[cls]
                        
                        # Draw bounding box
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                        
                        # Create label
                        label = f"{name} {conf:.2f}"
                        
                        # Draw label background
                        (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                        cv2.rectangle(annotated, (x1, y1 - label_h - 12), (x1 + label_w + 10, y1), color, -1)
                        cv2.putText(annotated, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        
                        # Log detection
                        ts = datetime.now().isoformat(sep=' ', timespec='seconds')
                        self.log.append((ts, name, "N/A", "N/A", 0))  # No priority/plate in general mode
                    
                    # Display object counts
                    y_offset = 30
                    total_objects = len(general_detections)
                    status_text = f"Total Objects: {total_objects} | Unique Classes: {len(self.object_counts)}"
                    cv2.putText(annotated, status_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(annotated, status_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
                    
                    # Display top 5 detected objects
                    y_offset += 35
                    sorted_counts = sorted(self.object_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    for obj_name, count in sorted_counts:
                        count_text = f"{obj_name}: {count}"
                        cv2.putText(annotated, count_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        cv2.putText(annotated, count_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
                        y_offset += 30
                    
                    # Store and display
                    self.last_annotated = annotated.copy()
                    cv2.imshow("General Object Detection (80+ Classes)", annotated)
                
                # =============== VEHICLE MODE (default) ===============
                else:
                    # Draw pedestrians if feature is enabled
                    if self.detect_pedestrians:
                        for ped in pedestrian_detections:
                            x1, y1, x2, y2 = ped['bbox']
                            conf = ped['conf']
                            
                            # Draw pedestrian bounding box in cyan
                            color = (255, 255, 0)  # Cyan for pedestrians
                            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                            
                            # Create label
                            label = f"Pedestrian {conf:.2f}"
                            
                            # Draw label background
                            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                            cv2.rectangle(annotated, (x1, y1 - label_h - 12), (x1 + label_w + 10, y1), color, -1)
                            cv2.putText(annotated, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                    
                    # Now draw only the nearest vehicles
                    for vehicle in nearest_vehicles:
                        x1, y1, x2, y2 = vehicle['bbox']
                        conf = vehicle['conf']
                        name = vehicle['name']
                        priority = vehicle['priority']
                        
                        frame_priorities.append(priority)
                        
                        # Try to detect license plate (only on OCR frames to improve performance)
                        license_plate = None
                        if run_ocr:
                            vehicle_id = f"{x1}_{y1}_{x2}_{y2}"  # Simple ID based on position
                            license_plate = self.detect_license_plate(frame, x1, y1, x2, y2, vehicle_id)
                            
                            # Debug: Show when we're processing
                            if license_plate:
                                print(f"✅ Vehicle: {name}, Plate: {license_plate}")
                        
                        # Choose color based on priority
                        if priority == 'HIGH':
                            color = (0, 0, 255)  # Red for high priority
                        elif priority == 'MEDIUM':
                            color = (0, 165, 255)  # Orange/Yellow for medium priority
                        else:  # LOW
                            color = (0, 255, 0)  # Green for low priority
                        
                        # Draw bounding box
                        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                        
                        # Create label with priority and license plate
                        if license_plate:
                            label = f"{name} {conf:.2f} [{priority}] | Plate: {license_plate}"
                        else:
                            label = f"{name} {conf:.2f} [{priority}]"
                        
                        # Draw label background with better visibility
                        (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                        cv2.rectangle(annotated, (x1, y1 - label_h - 12), (x1 + label_w + 10, y1), color, -1)
                        cv2.putText(annotated, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                        # Log detection with license plate and pedestrian count
                        ts = datetime.now().isoformat(sep=' ', timespec='seconds')
                        self.log.append((ts, name, priority, license_plate if license_plate else "N/A", self.pedestrian_count if self.detect_pedestrians else 0))
                    
                    # Determine highest priority and send LED command
                    if frame_priorities:
                        if 'HIGH' in frame_priorities:
                            new_priority = 'HIGH'
                        elif 'MEDIUM' in frame_priorities:
                            new_priority = 'MEDIUM'
                        else:
                            new_priority = 'LOW'
                        
                        # Only send command if priority changed
                        if new_priority != self.current_priority:
                            self.current_priority = new_priority
                            self.send_led_command(new_priority)
                    else:
                        # No vehicles detected, turn off LEDs
                        if self.current_priority != 'NONE':
                            self.current_priority = 'NONE'
                            self.send_led_command('NONE')
                    
                    # Display current priority status
                    if self.detect_pedestrians:
                        status_text = f"Priority: {self.current_priority} | Vehicles: {len(nearest_vehicles)}/{self.max_vehicles} | Pedestrians: {self.pedestrian_count}"
                    else:
                        status_text = f"Current Priority: {self.current_priority} | Tracking: {len(nearest_vehicles)}/{self.max_vehicles} vehicles"
                    cv2.putText(annotated, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(annotated, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)

                    # Store this annotated frame to prevent blinking
                    self.last_annotated = annotated.copy()
                    window_title = "Vehicle & Pedestrian Detection" if self.detect_pedestrians else "ESP32-CAM Vehicle Detection & Priority Classification"
                    cv2.imshow(window_title, annotated)
            else:
                # Show last annotated frame instead of raw frame to prevent blinking
                window_title = "Vehicle & Pedestrian Detection" if self.detect_pedestrians else "ESP32-CAM Vehicle Detection & Priority Classification"
                if self.last_annotated is not None:
                    cv2.imshow(window_title, self.last_annotated)
                else:
                    cv2.imshow(window_title, frame)
            
            key = cv2.waitKey(wait_time) & 0xFF
            if key == ord('q'):
                self.stop()
                break
            elif key == ord('e'):
                # Export Excel on 'e' key press
                try:
                    filename = self.export_excel()
                    print(f"✅ Excel exported: {filename}")
                except Exception as e:
                    print(f"❌ Export failed: {e}")

        self.cleanup()

    def stop(self):
        self.running = False

    def cleanup(self):
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        cv2.destroyAllWindows()

    def export_excel(self, filename=None):
        if openpyxl is None:
            raise RuntimeError("openpyxl not installed. Install with: pip install openpyxl")
        if filename is None:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"vehicle_detections_{now}.xlsx"

        wb = Workbook()
        ws = wb.active
        ws.title = "Vehicle Detections"
        
        # Add headers based on pedestrian detection mode
        if self.detect_pedestrians:
            ws.append(("Timestamp", "Vehicle Type", "Priority", "License Plate", "Pedestrians Nearby"))
            for ts, label, priority, plate, ped_count in list(self.log):
                ws.append((ts, label, priority, plate, ped_count))
        else:
            ws.append(("Timestamp", "Vehicle Type", "Priority", "License Plate"))
            for entry in list(self.log):
                # Handle both old format (4 items) and new format (5 items)
                if len(entry) == 5:
                    ts, label, priority, plate, _ = entry
                else:
                    ts, label, priority, plate = entry
                ws.append((ts, label, priority, plate))
        
        wb.save(filename)
        return filename


def start_tkinter_ui(detector: ESP32CamDetector):
    if tk is None:
        print("Tkinter not available. Install or run without GUI to export manually.")
        return

    root = tk.Tk()
    root.title("ESP32-CAM Detection Controls")

    def on_generate():
        try:
            filename = detector.export_excel()
            messagebox.showinfo("Excel Generated", f"Saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn = tk.Button(root, text="Generate Excel", command=on_generate, width=20, height=2)
    btn.pack(padx=10, pady=10)

    def on_close():
        detector.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Mode Object Detection System: Vehicle Priority Classification OR General Object Detection (80+ classes)",
        epilog="""
Examples:
  # VEHICLE MODE (default) - Detects vehicles with priority classification
  python new.py --ip 192.168.1.50
  python new.py --video traffic.mp4
  
  # GENERAL OBJECT DETECTION MODE - Detects 80+ everyday objects
  python new.py --video scene.mp4 --general-objects
  python new.py --ip http://192.168.1.100:8080/video --general-objects
  
  # IP Camera Sources:
  python new.py --ip http://192.168.1.100:8080/video  # IP Webcam (Android)
  python new.py --ip http://192.168.1.100:4747/video  # DroidCam
  python new.py --ip http://192.168.1.50/stream       # ESP32-CAM
  
  # WITH PEDESTRIAN DETECTION (Vehicle mode):
  python new.py --video traffic.mp4 --pedestrians
  python new.py --ip http://192.168.1.100:8080/video --pedestrians
  
  # Performance optimization:
  python new.py --video traffic.mp4 --scale 0.5         # Faster, lower quality
  python new.py --video traffic.mp4 --scale 1.0         # Best quality, slower
  
  # General objects WITH pedestrian tracking:
  python new.py --video scene.mp4 --general-objects --pedestrians
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--ip", help="Camera IP address or full stream URL (supports ESP32-CAM, IP Webcam, DroidCam, RTSP, etc.)")
    parser.add_argument("--stream-path", default="/stream", help="Stream path for ESP32-CAM (default: /stream, not used for full URLs)")
    parser.add_argument("--video", help="Path to video file for offline processing (alternative to --ip)")
    parser.add_argument("--scale", type=float, default=0.75, help="Processing scale factor (0.5-1.0, lower=faster, default=0.75)")
    parser.add_argument("--pedestrians", action="store_true", help="Enable pedestrian detection (detects people in the frame)")
    parser.add_argument("--general-objects", action="store_true", help="Enable general object detection mode (detects 80+ COCO classes instead of vehicle-only)")
    args = parser.parse_args()

    # Validate input
    if not args.ip and not args.video:
        print("Error: Must provide either --ip for camera stream or --video for video file")
        print("\n=== DETECTION MODES ===")
        print("  Vehicle Mode (default):     Detects cars, trucks, buses with priority")
        print("  General Objects Mode:       Detects 80+ objects (add --general-objects flag)")
        print("\n=== CAMERA SOURCES ===")
        print("  IP Webcam (Android):  http://YOUR_PHONE_IP:8080/video")
        print("  DroidCam:             http://YOUR_PHONE_IP:4747/video")
        print("  ESP32-CAM:            http://YOUR_ESP32_IP/stream")
        print("  Generic MJPEG:        http://YOUR_CAMERA_IP:PORT/stream")
        print("  RTSP Camera:          rtsp://YOUR_CAMERA_IP:554/stream")
        print("\n=== QUICK EXAMPLES ===")
        print("  Vehicle detection:           python new.py --video traffic.mp4")
        print("  General object detection:    python new.py --video scene.mp4 --general-objects")
        print("  With pedestrian tracking:    python new.py --video traffic.mp4 --pedestrians")
        print("\nRun 'python new.py --help' for more examples")
        parser.print_help()
        sys.exit(1)
    
    # Validate scale
    if args.scale <= 0 or args.scale > 1.0:
        print("Warning: Scale must be between 0.1 and 1.0. Using default 0.75")
        args.scale = 0.75

    detector = ESP32CamDetector(
        esp_ip=args.ip,
        stream_path=args.stream_path,
        video_path=args.video,
        process_scale=args.scale,
        detect_pedestrians=args.pedestrians,
        general_mode=args.general_objects
    )
    
    print(f"Processing at {args.scale*100:.0f}% resolution for better performance")
    
    # Display mode information
    if args.general_objects:
        print("🎯 GENERAL OBJECT DETECTION MODE - Detecting 80+ object classes from COCO dataset")
        print("   Objects: person, car, dog, cat, chair, laptop, phone, bottle, and 70+ more!")
    else:
        print("🚗 VEHICLE DETECTION MODE - Detecting vehicles with priority classification")
        print("   Add --general-objects flag for general object detection (80+ classes)")
    
    if args.pedestrians:
        print("🚶 Pedestrian detection ENABLED - Will highlight people in the frame")
    else:
        print("� Add --pedestrians flag to enable pedestrian tracking")

    # start tkinter UI in separate thread
    ui_thread = threading.Thread(target=start_tkinter_ui, args=(detector,), daemon=True)
    ui_thread.start()

    try:
        detector.run()
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
