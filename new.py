"""
ESP32-CAM Vehicle Detection and Priority Classification Client

Usage:
  - Upload the provided Arduino sketch to your ESP32-CAM (see README).
  - Make sure the ESP32-CAM is on your Wi-Fi and note its IP address.
  - Install Python requirements: pip install -r requirements.txt
  - Run with ESP32 stream: python new.py --ip 192.168.x.y
  - Run with video file: python new.py --video path/to/video.mp4

What this script does:
  - Connects to the ESP32-CAM MJPEG stream OR processes a video file
  - Runs vehicle detection using Ultralytics YOLO (yolov8n)
  - Classifies vehicles by priority:
      * HIGH: Emergency vehicles (ambulance, fire truck, police car)
      * MEDIUM: Commercial vehicles (bus, truck)
      * LOW: Personal vehicles (car, motorcycle, bicycle)
  - Controls ESP32 LEDs based on highest priority vehicle detected
  - Shows detections (labels + bounding boxes + priority) in a window
  - Keeps an in-memory log of detections (label + timestamp + priority)
  - Provides a Tkinter "Generate Excel" button which writes the log to an Excel file

Notes:
  - The script requires internet the first time to download YOLO weights via ultralytics.
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
    def __init__(self, esp_ip=None, stream_path="/stream", video_path=None):
        self.esp_ip = esp_ip
        self.video_path = video_path
        self.use_video = video_path is not None
        
        if esp_ip and esp_ip.startswith("http"):
            self.stream_url = esp_ip
        elif esp_ip:
            self.stream_url = f"http://{esp_ip}{stream_path}"
        else:
            self.stream_url = None

        self.cap = None
        self.model = None
        self.running = False
        self.log = deque()  # store (timestamp_iso, label, priority)
        self.frame = None
        self.current_priority = 'NONE'  # Track highest priority vehicle detected

    def load_model(self):
        if YOLO is None:
            raise RuntimeError("Ultralytics YOLO not available. Install with: pip install ultralytics")
        # use small model for speed
        self.model = YOLO("yolov8n.pt")

    def start_capture(self):
        if self.use_video:
            if not os.path.exists(self.video_path):
                raise RuntimeError(f"Video file not found: {self.video_path}")
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open video file at {self.video_path}")
        else:
            if not self.stream_url:
                raise RuntimeError("No ESP32 IP or video file provided")
            self.cap = cv2.VideoCapture(self.stream_url)
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open stream at {self.stream_url}")

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

        source_type = "video file" if self.use_video else "ESP32 stream"
        print(f"Starting vehicle detection from {source_type}. Press 'q' in the video window to quit.")
        
        frame_count = 0
        detection_interval = 1  # Process every frame for better detection
        
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

            # Detect vehicles on this frame
            if frame_count % detection_interval == 0:
                try:
                    results = self.model(frame)
                except Exception as e:
                    print("Detection error:", e)
                    time.sleep(0.5)
                    continue

                annotated = frame.copy()
                frame_priorities = []  # Track all priorities detected in this frame
                
                # Process detection results
                for r in results:
                    boxes = r.boxes
                    if boxes is None:
                        continue
                    for box in boxes:
                        xyxy = box.xyxy[0].cpu().numpy() if hasattr(box.xyxy[0], 'cpu') else box.xyxy[0].numpy()
                        x1, y1, x2, y2 = map(int, xyxy[:4])
                        conf = float(box.conf[0]) if hasattr(box, 'conf') and len(box.conf) else 0.0
                        cls = int(box.cls[0]) if hasattr(box, 'cls') and len(box.cls) else None
                        name = r.names[cls] if (cls is not None and r.names is not None and cls in r.names) else str(cls)

                        # Classify vehicle priority
                        priority = self.classify_vehicle_priority(name)
                        
                        if priority:  # Only process if it's a vehicle
                            frame_priorities.append(priority)
                            
                            # Choose color based on priority
                            if priority == 'HIGH':
                                color = (0, 0, 255)  # Red for high priority
                            elif priority == 'MEDIUM':
                                color = (0, 165, 255)  # Orange/Yellow for medium priority
                            else:  # LOW
                                color = (0, 255, 0)  # Green for low priority
                            
                            # Draw bounding box
                            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                            
                            # Create label with priority
                            label = f"{name} {conf:.2f} [{priority}]"
                            
                            # Draw label background
                            (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                            cv2.rectangle(annotated, (x1, y1 - label_h - 10), (x1 + label_w, y1), color, -1)
                            cv2.putText(annotated, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                            # Log detection
                            ts = datetime.now().isoformat(sep=' ', timespec='seconds')
                            self.log.append((ts, name, priority))
                
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
                status_text = f"Current Priority: {self.current_priority}"
                cv2.putText(annotated, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(annotated, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

                cv2.imshow("ESP32-CAM Vehicle Detection & Priority Classification", annotated)
            else:
                # Just show the frame without processing
                cv2.imshow("ESP32-CAM Vehicle Detection & Priority Classification", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.stop()
                break

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
        ws.append(("Timestamp", "Vehicle Type", "Priority"))
        for ts, label, priority in list(self.log):
            ws.append((ts, label, priority))
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
    parser = argparse.ArgumentParser(description="ESP32-CAM vehicle detection and priority classification client")
    parser.add_argument("--ip", help="ESP32-CAM IP address or full stream URL (e.g. 192.168.1.50 or http://192.168.1.50/stream)")
    parser.add_argument("--stream-path", default="/stream", help="stream path used by ESP sketch (default /stream)")
    parser.add_argument("--video", help="Path to video file for offline processing (alternative to --ip)")
    args = parser.parse_args()

    # Validate input
    if not args.ip and not args.video:
        print("Error: Must provide either --ip for ESP32-CAM stream or --video for video file")
        parser.print_help()
        sys.exit(1)

    detector = ESP32CamDetector(
        esp_ip=args.ip,
        stream_path=args.stream_path,
        video_path=args.video
    )

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
