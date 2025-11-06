# 📷 Real-Time Object Detection System

An advanced real-time object detection system powered by YOLOv8, featuring specialized implementations for vehicle detection with priority classification, pedestrian tracking, and license plate recognition using EasyOCR.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8-green.svg)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

-   [Overview](#-project-overview)
-   [Features](#-key-features)
-   [Applications](#-real-world-applications)
-   [System Requirements](#-system-requirements)
-   [Installation](#-installation)
-   [Quick Start](#-quick-start)
-   [Usage Examples](#-usage-examples)
-   [ESP32-CAM Setup](#-esp32-cam-hardware-setup)
-   [IP Camera Setup](#-ip-camera-setup)
-   [Web Dashboard](#-web-dashboard)
-   [API Documentation](#-api-documentation)
-   [Troubleshooting](#-troubleshooting)
-   [Performance Optimization](#-performance-optimization)

---

## 🎯 Project Overview

This is a **versatile object detection system** built on YOLOv8, designed to detect and classify various objects in real-time. The project showcases its capabilities through a comprehensive **vehicle detection and traffic management application**.

### Core Technology

-   **YOLOv8** (You Only Look Once) - State-of-the-art object detection
-   **EasyOCR** - Optical Character Recognition for text extraction
-   **OpenCV** - Real-time computer vision processing
-   **ESP32-CAM** - Embedded camera integration
-   **Flask & React** - Modern web dashboard

### Primary Application: Intelligent Traffic Management

The system demonstrates object detection capabilities through a fully-featured traffic management solution that includes:

-   Multi-class vehicle detection and classification
-   Emergency vehicle priority identification
-   Pedestrian detection and counting
-   Automatic license plate recognition
-   Real-time analytics and data logging

### Extensibility

While the current implementation focuses on traffic management, the underlying object detection framework can be adapted for:

-   Retail analytics (customer counting, product detection)
-   Security surveillance (person detection, anomaly detection)
-   Industrial automation (defect detection, quality control)
-   Wildlife monitoring (animal detection and tracking)
-   Healthcare applications (PPE detection, social distancing)

---

## 🎯 Key Features

### Core Object Detection Capabilities

-   🎯 **YOLOv8 Integration** - Industry-leading object detection model
-   ⚡ **Real-time Processing** - 30-40 FPS on standard hardware
-   🎨 **Multi-class Detection** - Supports 80+ object classes from COCO dataset
-   📊 **Confidence Scoring** - Adjustable detection thresholds
-   🔄 **Multiple Input Sources** - Video files, live cameras, IP streams, ESP32-CAM

-   🔄 **Multiple Input Sources** - Video files, live cameras, IP streams, ESP32-CAM

### Vehicle Detection Application (Primary Implementation)

#### Vehicle Classification & Tracking

-   🚗 **Multi-Vehicle Detection** - Cars, trucks, buses, motorcycles, bicycles
-   ✅ **Smart Tracking** - Tracks 5 nearest vehicles for optimal performance
-   📏 **Distance Calculation** - Automatically prioritizes closest vehicles
-   🎯 **High Accuracy** - 30-40 FPS processing speed

#### Intelligent Priority System

-   🔴 **HIGH Priority**: Emergency vehicles (Ambulance, Fire Truck, Police)
-   🟠 **MEDIUM Priority**: Commercial vehicles (Bus, Truck)
-   🟢 **LOW Priority**: Personal vehicles (Car, Motorcycle, Bicycle)
-   💡 **LED Indicators** - Real-time priority visualization via ESP32-CAM

#### License Plate Recognition (LPR)

-   🔍 **EasyOCR Integration** - Advanced OCR with 85%+ accuracy
-   🎯 **Smart Preprocessing** - Bilateral filtering, adaptive thresholding
-   ⚡ **Performance Optimized** - OCR runs every 15th frame (configurable)
-   💾 **Caching System** - 3-second cache to prevent duplicate reads
-   📊 **Excel Export** - Automatic logging with timestamps

#### Pedestrian Detection

-   🚶 **Person Detection** - Identifies pedestrians in traffic scenes
-   📊 **Count Tracking** - Real-time pedestrian counting
-   🔵 **Visual Indicators** - Cyan bounding boxes for pedestrians
-   📈 **Analytics** - Pedestrian count in Excel reports
-   🛡️ **Safety Monitoring** - Pedestrian proximity alerts

### Hardware Integration

-   📷 **ESP32-CAM Support** - Native wireless camera integration
-   📱 **IP Camera Apps** - IP Webcam, DroidCam, generic MJPEG/RTSP
-   💡 **LED Control** - RGB LED indicators for priority status
-   🔌 **WiFi Streaming** - Real-time MJPEG stream processing

### Data Management

-   📊 **Excel Export** - One-click export with press 'e' key
-   🗂️ **Structured Logging** - Timestamp, vehicle type, priority, plate, pedestrians
-   🌐 **REST API** - Flask backend for web dashboard integration
-   📈 **Real-time Stats** - Live detection metrics

---

## 🌍 Real-World Applications

### Primary Use Case: Traffic Management & Smart Transportation 🚦

This object detection system is currently implemented as a comprehensive **Intelligent Traffic Management Solution**:

#### 1. **Smart Traffic Control Systems**

-   **Smart Traffic Lights**: Automatically adjust signal timing based on vehicle priority
-   **Emergency Vehicle Priority**: Give green light to ambulances and fire trucks
-   **Congestion Management**: Analyze traffic patterns and optimize flow
-   **Peak Hour Analysis**: Track vehicle types during rush hours

#### 2. **Smart City Solutions** 🏙️

-   **Automated Toll Collection**: License plate recognition for toll booths
-   **Parking Management**: Monitor parking lot occupancy and vehicle tracking
-   **Access Control**: Automated gate systems for residential/commercial areas
-   **Security Surveillance**: Track and log vehicle movements

#### 3. **Law Enforcement & Public Safety** 👮

-   **Speed Enforcement**: Integrate with speed cameras for automated ticketing
-   **Stolen Vehicle Detection**: Real-time ANPR for wanted vehicle alerts
-   **Traffic Violation Monitoring**: Red light violations, wrong-way detection
-   **Evidence Collection**: Timestamped vehicle logs for investigations

#### 4. **Transportation & Logistics** 🚚

-   **Fleet Management**: Track company vehicles and deliveries
-   **Loading Bay Automation**: Identify and prioritize delivery trucks
-   **Warehouse Security**: Monitor vehicle entry/exit
-   **Route Optimization**: Analyze traffic patterns for efficient routing

#### 5. **Emergency Response** 🚨

-   **Emergency Response**: Automatic priority for ambulances and fire trucks
-   **Pedestrian Safety**: Detect pedestrians near crosswalks
-   **School Zone Monitoring**: Track vehicles near schools
-   **Accident Prevention**: Identify dangerous situations

#### 6. **Commercial Applications** 💼

-   **Drive-Through Automation**: Vehicle detection for restaurants/banks
-   **Car Wash Management**: Automatic vehicle type identification
-   **Service Station Monitoring**: Track customer vehicles
-   **Retail Analytics**: Analyze customer arrival patterns

#### 7. **Research & Development** 🔬

-   **Traffic Pattern Analysis**: Study urban mobility patterns
-   **AI Model Training**: Generate annotated datasets
-   **Smart Infrastructure**: Test autonomous vehicle interactions
-   **Behavioral Studies**: Analyze driver and pedestrian behavior

---

### 🔄 Potential Applications (Beyond Traffic)

The object detection framework can be easily adapted for:

-   **🏪 Retail & Commerce**: Customer counting, queue management, shelf monitoring
-   **🏭 Industrial**: Manufacturing defect detection, safety compliance, inventory tracking
-   **🏥 Healthcare**: PPE detection, social distancing monitoring, patient tracking
-   **🌾 Agriculture**: Crop monitoring, pest detection, livestock tracking
-   **🏗️ Construction**: Safety equipment detection, progress monitoring, hazard identification
-   **🌲 Wildlife Conservation**: Animal detection and counting, behavior analysis
-   **🏠 Home Security**: Intruder detection, package delivery monitoring, pet tracking
-   **⚽ Sports Analytics**: Player tracking, ball detection, performance analysis

---

## 💻 System Requirements

### Minimum Requirements

-   **OS**: Windows 10/11, Linux, macOS
-   **CPU**: Intel i5 or equivalent
-   **RAM**: 4GB
-   **Python**: 3.8 or higher
-   **Storage**: 2GB free space
-   **Expected Performance**: 15-20 FPS

### Recommended

-   **OS**: Windows 11 / Ubuntu 22.04
-   **CPU**: Intel i7 / AMD Ryzen 7 or better
-   **RAM**: 8GB or more
-   **Python**: 3.10+
-   **GPU**: NVIDIA GPU with CUDA (optional, for faster processing)
-   **Storage**: 5GB free space
-   **Expected Performance**: 30-40 FPS

### Optimal (GPU Enabled)

-   **CPU**: Intel i9 / AMD Ryzen 9
-   **RAM**: 16GB+
-   **GPU**: NVIDIA GTX 1060 or better with CUDA
-   **Storage**: 10GB SSD
-   **Expected Performance**: 60+ FPS

---

## 📦 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/develo-oper-piyush/Object-detection---Copy.git
cd Object-detection---Copy
```

> 💡 **Note**: This is a general-purpose object detection system. The current implementation demonstrates vehicle detection capabilities, but the framework supports detection of 80+ object classes from the COCO dataset.

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Required Packages:**

-   `ultralytics` - YOLOv8 object detection model
-   `opencv-python` - Computer vision and image processing
-   `easyocr` - OCR for license plate recognition (traffic application)
-   `openpyxl` - Excel export functionality
-   `torch` & `torchvision` - PyTorch deep learning backend
-   `Pillow` - Image processing utilities
-   `requests` - HTTP requests for camera streams
-   `flask` & `flask-cors` - REST API backend (optional)

### Step 4: Download YOLO Model

The YOLOv8n model will download automatically on first run. Or download manually:

```bash
# YOLOv8 model for object detection
# yolov8n.pt (~6MB) downloads on first execution
# Supports 80+ object classes from COCO dataset
```

> 🎯 **Supported Object Classes**: The YOLO model can detect: person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush.

### Step 5: Verify Installation

```bash
python new.py --help
```

You should see the help menu with all available options.

---

## 🚀 Quick Start

> 📌 **Current Implementation**: The examples below demonstrate the **vehicle detection application**. The system can be modified to detect any of the 80+ COCO object classes.

### Option 1: Video File (Fastest Way to Test)

```bash
# Basic usage
python new.py --video traffic.mp4

# With pedestrian detection
python new.py --video traffic.mp4 --pedestrians

# Maximum speed
python new.py --video traffic.mp4 --scale 0.5

# Best quality
python new.py --video traffic.mp4 --scale 1.0
```

### Option 2: IP Camera (Phone Camera)

```bash
# Using IP Webcam app
python new.py --ip http://192.168.1.100:8080/video

# With pedestrian detection
python new.py --ip http://192.168.1.100:8080/video --pedestrians

# Using DroidCam
python new.py --ip http://192.168.1.100:4747/video
```

### Option 3: ESP32-CAM

```bash
# Using ESP32-CAM (after setup)
python new.py --ip 192.168.1.50

# With custom stream path
python new.py --ip http://192.168.1.50/stream
```

---

## 📱 Usage Examples

> 🎯 **Note**: These examples showcase the vehicle detection application. To detect other objects, modify the detection classes in `new.py`.

### 1. Basic Vehicle Detection (Video File)

```bash
python new.py --video traffic.mp4
```

**What it does:**

-   Detects vehicles at 75% resolution (default)
-   Tracks 5 nearest vehicles
-   Shows priority classification
-   Processes at ~30 FPS

### 2. Vehicle + Pedestrian Detection

```bash
python new.py --video traffic.mp4 --pedestrians
```

**What it does:**

-   Detects both vehicles AND pedestrians
-   Shows pedestrian count in status bar
-   Cyan boxes for pedestrians
-   Exports pedestrian data to Excel

### 3. License Plate Recognition

```bash
python new.py --video traffic.mp4 --scale 1.0
```

**What it does:**

-   Full resolution for better OCR accuracy
-   Detects and reads license plates
-   Displays plates on bounding boxes
-   Logs plates in Excel file

### 4. IP Camera Live Stream

```bash
python new.py --ip http://192.168.1.100:8080/video --pedestrians
```

**What it does:**

-   Real-time detection from phone camera
-   Detects vehicles and pedestrians
-   No artificial FPS limit
-   Press 'e' to export data

### 5. Maximum Performance Mode

```bash
python new.py --video traffic.mp4 --scale 0.5
```

**What it does:**

-   Processes at 50% resolution
-   Achieves 40-50 FPS
-   Lower quality but faster
-   Good for real-time monitoring

### 6. High Quality Mode (Best OCR)

```bash
python new.py --video traffic.mp4 --scale 1.0 --pedestrians
```

**What it does:**

-   Full resolution processing
-   Best license plate reading
-   Pedestrian detection enabled
-   ~15-20 FPS

---

## 🔧 ESP32-CAM Hardware Setup

> 🔌 **Hardware Integration**: The ESP32-CAM enables edge deployment of the object detection system. While the current setup demonstrates traffic monitoring, the same hardware can be used for various IoT-based detection applications.

### Components Required

| Component                     | Quantity | Purpose                                |
| ----------------------------- | -------- | -------------------------------------- |
| ESP32-CAM (AI-Thinker)        | 1        | Camera module with WiFi                |
| **MicroSD Card (4GB-32GB)**   | **1**    | **Required for camera initialization** |
| FTDI Programmer (FT232RL)     | 1        | Upload code to ESP32                   |
| Female-to-Female Jumper Wires | 6        | Connections                            |
| Micro USB Cable               | 1        | Power FTDI                             |
| Red LED                       | 1        | High priority indicator                |
| Yellow/Orange LED             | 1        | Medium priority indicator              |
| Green LED                     | 1        | Low priority indicator                 |
| 220Ω Resistors                | 3        | Current limiting for LEDs              |
| Breadboard                    | 1        | Circuit assembly                       |
| 5V Power Supply               | 1        | Power ESP32-CAM (optional)             |

> ⚠️ **IMPORTANT**: MicroSD card is REQUIRED even for streaming mode! The ESP32-CAM firmware needs it for camera initialization and frame buffering.

### Circuit Connections

#### FTDI to ESP32-CAM (Programming Mode)

```
FTDI Programmer → ESP32-CAM
━━━━━━━━━━━━━━━━━━━━━━━━━
5V    →  5V
GND   →  GND
TX    →  RX (U0R)
RX    →  TX (U0T)
GND   →  GPIO 0 (for programming only)
```

#### LED Connections (After Programming)

```
ESP32-CAM GPIO → LED Circuit
━━━━━━━━━━━━━━━━━━━━━━━━━━━
GPIO 12  →  220Ω Resistor  →  Red LED (+)    →  GND
GPIO 13  →  220Ω Resistor  →  Yellow LED (+) →  GND
GPIO 15  →  220Ω Resistor  →  Green LED (+)  →  GND
```

### Step-by-Step Setup

#### Step 1: Prepare MicroSD Card

> ⚠️ **DO THIS FIRST!** ESP32-CAM will NOT work without a properly formatted microSD card.

1. **Get a microSD card**:

    - Size: 4GB to 32GB (32GB recommended)
    - Speed: Class 10 or UHS-1
    - Brand: SanDisk, Samsung, Kingston (reliable brands)

2. **Format the card to FAT32**:

    **Windows:**

    - Insert card into PC
    - Right-click the drive → Format
    - File System: **FAT32**
    - Allocation Unit: **Default**
    - Click **Start**

    **Mac:**

    - Open Disk Utility
    - Select the SD card
    - Click **Erase**
    - Format: **MS-DOS (FAT)**
    - Click **Erase**

3. **Insert into ESP32-CAM**:
    - Metal contacts facing UP (toward the camera lens)
    - Push until it clicks
    - Card should be flush with the board edge

#### Step 2: Install Arduino IDE

1. Download from https://www.arduino.cc/en/software
2. Install Arduino IDE (version 2.0+ recommended)
3. Open Arduino IDE

#### Step 3: Add ESP32 Board Support

1. Go to **File → Preferences**
2. Add this URL to "Additional Board Manager URLs":
    ```
    https://dl.espressif.com/dl/package_esp32_index.json
    ```
3. Click **OK**
4. Go to **Tools → Board → Boards Manager**
5. Search for "ESP32"
6. Install "**esp32 by Espressif Systems**" (latest version)

#### Step 4: Select Board & Port

1. Go to **Tools → Board → ESP32 Arduino**
2. Select "**AI Thinker ESP32-CAM**"
3. Go to **Tools → Port**
4. Select your FTDI programmer port (e.g., COM3, /dev/ttyUSB0)

#### Step 5: Configure Upload Settings

```
Board: "AI Thinker ESP32-CAM"
Upload Speed: "115200"
CPU Frequency: "240MHz (WiFi/BT)"
Flash Frequency: "80MHz"
Flash Mode: "QIO"
Flash Size: "4MB (32Mb)"
Partition Scheme: "Default 4MB with spiffs"
Core Debug Level: "None"
Port: [Your FTDI Port]
```

#### Step 6: Modify Arduino Sketch

1. Open `esp32_cam_stream.ino` from the project folder
2. **Update WiFi credentials:**
    ```cpp
    const char* WIFI_SSID = "YOUR_WIFI_NAME";
    const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
    ```
3. Save the file

#### Step 7: Wire for Programming

1. Connect FTDI to ESP32-CAM as shown in table above
2. **Important**: Connect GPIO 0 to GND (programming mode)
3. Connect USB cable to FTDI
4. ESP32-CAM should power on (LED may flash)

#### Step 8: Upload Code

1. Click **Upload** button (→) in Arduino IDE
2. Wait for "Connecting..." message
3. **Press and hold RESET button** on ESP32-CAM
4. Release when upload starts ("Writing at 0x00001000...")
5. Wait for "Hard resetting via RTS pin..." message
6. Upload complete! ✅

#### Step 9: Switch to Normal Mode

1. **Disconnect GPIO 0 from GND**
2. Press RESET button on ESP32-CAM
3. Open **Serial Monitor** (115200 baud)
4. You should see:
    ```
    Connecting to WiFi.....
    Connected. IP: 192.168.1.50
    Camera Stream Ready. Use /stream for MJPEG.
    ```
5. **Note the IP address** (e.g., 192.168.1.50)

#### Step 10: Connect LEDs (Optional)

1. Remove FTDI connections
2. Connect LEDs as shown in LED table above
3. Power ESP32-CAM with 5V supply (or keep FTDI connected)
4. LEDs will indicate vehicle priority

#### Step 11: Test Camera Stream

1. Open web browser
2. Navigate to: `http://YOUR_ESP32_IP/stream`
3. You should see live camera feed
4. Test LED control: `http://YOUR_ESP32_IP/led?color=red`

### Common ESP32 Issues

**Problem: "Failed to connect to ESP32"**

-   Solution: Make sure GPIO 0 is connected to GND before uploading
-   Try pressing RESET button while clicking Upload
-   Check FTDI connections (TX↔RX should be crossed)
-   Try lower upload speed (Tools → Upload Speed → 115200)

**Problem: "Brownout detector was triggered"**

-   Solution: ESP32-CAM needs stable 5V power
-   Use external 5V power supply (not just USB)
-   Add 100µF capacitor across 5V and GND

**Problem: "Camera init failed"**

-   Solution: **Make sure microSD card is inserted and formatted as FAT32**
-   Check camera ribbon cable is properly inserted
-   Try different power supply
-   Try a different microSD card (some cards are incompatible)
-   Reset ESP32 and try again

**Problem: "No SD card detected"**

-   Solution: Reinsert the microSD card (contacts facing up)
-   Format card to FAT32 (not exFAT or NTFS)
-   Try a different card (4GB-32GB, Class 10)
-   Clean the metal contacts with a soft cloth

**Problem: "WiFi won't connect"**

-   Solution: Double-check SSID and password
-   Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
-   Move ESP32 closer to router

---

## 📱 IP Camera Setup

### Option 1: IP Webcam (Android) - RECOMMENDED

#### Installation

1. Download **IP Webcam** from Google Play Store
2. Install and open the app
3. Grant camera and microphone permissions

#### Configuration

1. Scroll down in the app
2. **Video Preferences**:
    - Resolution: 1280x720 (720p) or higher
    - Quality: 80-90%
    - FPS limit: 30
    - Video encoder: MJPEG (recommended)
3. **Connection**:
    - Scroll to bottom
    - Tap **Start server**
    - Note the IP address (e.g., `http://192.168.1.100:8080`)

#### Usage

```bash
# Replace with your phone's IP
python new.py --ip http://192.168.1.100:8080/video

# With pedestrian detection
python new.py --ip http://192.168.1.100:8080/video --pedestrians
```

### Option 2: DroidCam (Android/iOS)

#### Installation

1. Download **DroidCam** from Play Store / App Store
2. Install on phone
3. (Optional) Install DroidCam Client on PC

#### Usage

```bash
# Default DroidCam port is 4747
python new.py --ip http://192.168.1.100:4747/video
```

### Option 3: Generic MJPEG/RTSP Camera

```bash
# MJPEG camera
python new.py --ip http://CAMERA_IP:PORT/stream

# RTSP camera
python new.py --ip rtsp://CAMERA_IP:554/stream

# With authentication
python new.py --ip rtsp://username:password@CAMERA_IP:554/stream
```

### Finding Your Phone's IP Address

**Android:**

1. Settings → WiFi
2. Tap connected network
3. Look for "IP address"

**iOS:**

1. Settings → WiFi
2. Tap (i) icon next to network
3. Look for "IP Address"

**Or check in the camera app** - Most apps display the IP when server starts

---

## 🌐 Web Dashboard

### Setup

```bash
cd Web-Dashboard/Web-Dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

Dashboard will be available at: `http://localhost:3000`

### Start Flask API (for live data)

```bash
# In project root directory
python api.py
```

API will be available at: `http://localhost:5000`

### Features

-   📊 Real-time detection statistics
-   📈 Priority distribution charts
-   📋 Recent detections table
-   📹 Live camera feed preview
-   📥 Excel export button
-   🎨 Animated dot grid background
-   📱 Responsive design

---

## 🔌 API Documentation

### Start API Server

```bash
python api.py
```

### Endpoints

#### 1. Export Excel (Open in Browser)

```
GET http://localhost:5000/api/export
```

**Response**: Excel file opened in browser

#### 2. Download Excel

```
GET http://localhost:5000/api/export/download
```

**Response**: Excel file download

#### 3. Get Statistics

```
GET http://localhost:5000/api/stats
```

**Response**:

```json
{
    "totalDetections": 147,
    "highPriority": 12,
    "mediumPriority": 45,
    "lowPriority": 90,
    "withPlates": 98,
    "withoutPlates": 49
}
```

#### 4. Get Recent Detections

```
GET http://localhost:5000/api/detections
```

**Response**: Array of detection objects

#### 5. Health Check

```
GET http://localhost:5000/api/health
```

**Response**:

```json
{
    "status": "ok",
    "message": "API is running"
}
```

---

## ⌨️ Keyboard Controls

While the detection window is active:

| Key   | Action                          |
| ----- | ------------------------------- |
| `q`   | Quit the application            |
| `e`   | Export detections to Excel file |
| `ESC` | Quit (alternative)              |

---

## 📊 Excel Export Format

### Without Pedestrians

| Timestamp           | Vehicle Type | Priority | License Plate |
| ------------------- | ------------ | -------- | ------------- |
| 2025-11-06 14:30:15 | car          | LOW      | ABC1234       |
| 2025-11-06 14:30:18 | ambulance    | HIGH     | EMG911        |

### With Pedestrians (--pedestrians flag)

| Timestamp           | Vehicle Type | Priority | License Plate | Pedestrians Nearby |
| ------------------- | ------------ | -------- | ------------- | ------------------ |
| 2025-11-06 14:30:15 | car          | LOW      | ABC1234       | 2                  |
| 2025-11-06 14:30:18 | ambulance    | HIGH     | EMG911        | 5                  |

Files are saved as: `vehicle_detections_YYYYMMDD_HHMMSS.xlsx`

---

## 🔧 Troubleshooting

### Video Playback Issues

**Problem: Video is laggy/slow**

```bash
# Solution 1: Lower resolution
python new.py --video traffic.mp4 --scale 0.5

# Solution 2: Skip more frames (edit new.py)
# Change detection_interval from 3 to 5
```

**Problem: Boxes are blinking**

-   Fixed! The system now stores last frame to prevent blinking
-   Update to latest version

### Camera Connection Issues

**Problem: "Failed to open stream"**

```bash
# Check 1: Verify IP address
ping 192.168.1.100

# Check 2: Test in browser
# Open: http://192.168.1.100:8080

# Check 3: Same WiFi network
# Ensure phone and PC are on same network

# Check 4: Firewall
# Temporarily disable firewall to test
```

**Problem: Stream connects but no video**

```bash
# Try different URL format
python new.py --ip http://IP:PORT/video     # IP Webcam
python new.py --ip http://IP:PORT/mjpeg     # Some cameras
python new.py --ip http://IP:PORT/stream    # ESP32-CAM
```

### Detection Issues

**Problem: Not detecting vehicles**

-   Make sure camera is pointing at vehicles
-   Check lighting conditions
-   Try full resolution: `--scale 1.0`
-   Ensure YOLO model downloaded (yolov8n.pt in folder)

**Problem: License plates not detected**

```bash
# Use full resolution
python new.py --video traffic.mp4 --scale 1.0

# Check if EasyOCR is installed
pip install easyocr

# Plates must be clearly visible (minimum 50px height)
```

**Problem: Too slow with pedestrians**

```bash
# Lower resolution
python new.py --video traffic.mp4 --pedestrians --scale 0.5
```

### Installation Issues

**Problem: "No module named 'ultralytics'"**

```bash
pip install ultralytics
```

**Problem: "No module named 'easyocr'"**

```bash
pip install easyocr
```

**Problem: CUDA/GPU errors**

```bash
# Use CPU mode (automatic fallback)
# Or install CUDA toolkit for GPU acceleration
```

---

## ⚡ Performance Optimization

### Speed vs Quality Trade-offs

| Scale | Resolution | FPS   | Detection Quality | OCR Quality | Use Case                  |
| ----- | ---------- | ----- | ----------------- | ----------- | ------------------------- |
| 0.5   | 50%        | 40-50 | Good              | Medium      | Real-time monitoring      |
| 0.75  | 75%        | 25-35 | Very Good         | Good        | **Default (recommended)** |
| 1.0   | 100%       | 15-20 | Excellent         | Excellent   | License plate reading     |

### Configuration Options

Edit `new.py` to customize:

```python
# Line ~340
detection_interval = 3  # Process every Nth frame (1-5)
# Lower = more detections, slower
# Higher = fewer detections, faster

# Line ~341
ocr_interval = 15  # Run OCR every Nth frame (5-30)
# Lower = more plate reads, slower
# Higher = fewer plate reads, faster

# Line ~108
self.max_vehicles = 5  # Max vehicles to track (1-10)
# Lower = faster
# Higher = more vehicles tracked
```

### GPU Acceleration

To enable GPU for faster processing:

1. Install CUDA Toolkit
2. Install GPU-enabled PyTorch:
    ```bash
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    ```
3. Edit `new.py` line ~120:
    ```python
    self.ocr_reader = easyocr.Reader(['en'], gpu=True)  # Change to True
    ```

Expected improvement: 2-3x faster OCR processing

---

## 📁 Project Structure

```
Object-detection/
├── new.py                          # Main object detection script (vehicle detection implementation)
├── api.py                          # Flask REST API backend
├── esp32_cam_stream.ino           # ESP32-CAM firmware for IoT camera integration
├── requirements.txt                # Python dependencies
├── yolov8n.pt                     # YOLOv8 model (80+ COCO classes)
├── README.md                       # This file
├── API_SETUP.md                   # API documentation
├── IP_CAMERA_SETUP.md             # IP camera configuration guide
├── PERFORMANCE_GUIDE.md           # Performance optimization tips
├── WIRING_DIAGRAM.md              # ESP32-CAM wiring diagrams
├── Web-Dashboard/                 # React-based web dashboard
│   └── Web-Dashboard/
│       ├── src/                    # React components
│       ├── public/                 # Static assets
│       ├── package.json            # Node.js dependencies
│       └── vite.config.js          # Vite build configuration
└── vehicle_detections_*.xlsx      # Exported detection data
```

---

## 🎓 Usage Tips

### Best Practices

1. **Camera Positioning**

    - Mount camera 3-10 meters from road
    - Angle slightly downward for better plate visibility
    - Ensure good lighting (natural or artificial)
    - Avoid direct sunlight/headlights in lens

2. **Performance**

    - Start with default settings (`--scale 0.75`)
    - Use `--scale 0.5` for real-time monitoring
    - Use `--scale 1.0` for license plate reading
    - Close other applications for better performance

3. **Data Collection**

    - Press 'e' periodically to export data
    - Excel files are timestamped automatically
    - Keep detection running in background
    - Review logs for traffic patterns

4. **Network**
    - Use 2.4GHz WiFi for ESP32-CAM
    - Keep phone/camera close to router
    - Use wired connection for PC if possible
    - Reduce video quality if network is slow

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📞 Support

-   **Issues**: [GitHub Issues](https://github.com/develo-oper-piyush/Object-detection---Copy/issues)
-   **Documentation**: Check `*.md` files in project folder
-   **API Docs**: `API_SETUP.md`
-   **IP Camera Guide**: `IP_CAMERA_SETUP.md`

---

## 🎉 Acknowledgments

-   **Ultralytics** - YOLOv8 implementation
-   **EasyOCR** - License plate recognition
-   **OpenCV** - Computer vision library
-   **Espressif** - ESP32-CAM platform

---

## 📈 Changelog

### Version 2.0.0 (Latest)

-   ✅ Added pedestrian detection feature
-   ✅ Fixed blinking boxes issue
-   ✅ Improved frame rate (30-40 FPS)
-   ✅ Limited tracking to 5 nearest vehicles
-   ✅ Added Flask API backend
-   ✅ React web dashboard
-   ✅ IP camera support (IP Webcam, DroidCam, RTSP)
-   ✅ Performance optimization (configurable scale)

### Version 1.0.0

-   Initial release with vehicle detection
-   License plate recognition
-   ESP32-CAM support
-   Excel export

---

## 🚀 What's Next?

### Planned Features for Object Detection System:

**Core Detection Enhancements:**

-   [ ] Custom object class training (train YOLO on specific use cases)
-   [ ] Multi-camera synchronization and fusion
-   [ ] Object tracking across frames (DeepSORT integration)
-   [ ] 3D object detection and depth estimation
-   [ ] Real-time object counting and analytics

**Infrastructure & Deployment:**

-   [ ] Database integration (MySQL/PostgreSQL) for persistent storage
-   [ ] Cloud deployment options (AWS, Azure, GCP)
-   [ ] Docker containerization for easy deployment
-   [ ] Kubernetes orchestration for scalability
-   [ ] Edge AI optimization (TensorRT, OpenVINO)

**Application Expansions:**

-   [ ] Retail analytics module (customer tracking, heatmaps)
-   [ ] Industrial quality control system
-   [ ] Wildlife monitoring application
-   [ ] Healthcare safety compliance checker
-   [ ] Agriculture crop/pest detection system

**User Interface:**

-   [ ] Mobile app (React Native) for remote monitoring
-   [ ] Advanced analytics dashboard with historical data
-   [ ] Real-time notification system (email, SMS, push)
-   [ ] Multi-language support for global deployment

**Traffic Application Specific:**

-   [ ] AI-based traffic prediction and forecasting
-   [ ] Integration with traffic light control systems
-   [ ] Vehicle re-identification across multiple cameras
-   [ ] Automatic incident detection and alerting

---

**Made with ❤️ for Computer Vision, AI, and Smart Solutions**

_A versatile object detection system powered by YOLOv8 • Currently showcasing intelligent traffic management • Extensible to unlimited applications_

_Last Updated: November 6, 2025_
