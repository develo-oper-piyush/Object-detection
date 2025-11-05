# Quick Start Guide - Vehicle Detection System

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```cmd
python -m pip install -r requirements.txt
```

### Step 2: Test Your Setup

```cmd
python test_system.py
```

### Step 3: Run with Video File

Place a video file (e.g., `traffic.mp4`) in this folder, then:

```cmd
python new.py --video traffic.mp4
```

### Step 4: (Optional) Run with ESP32-CAM

```cmd
python new.py --ip 192.168.1.50
```

## 📋 ESP32-CAM Setup Checklist

-   [ ] Arduino IDE installed
-   [ ] ESP32 board support added to Arduino IDE
-   [ ] WiFi credentials updated in `esp32_cam_stream.ino`
-   [ ] Code uploaded to ESP32-CAM
-   [ ] IP address noted from Serial Monitor
-   [ ] LEDs connected:
    -   [ ] Red LED → GPIO 12 (+ 220Ω resistor)
    -   [ ] Yellow LED → GPIO 13 (+ 220Ω resistor)
    -   [ ] Green LED → GPIO 15 (+ 220Ω resistor)

## 🎨 LED Behavior

| Priority | Vehicle Types                 | LED Color  |
| -------- | ----------------------------- | ---------- |
| HIGH     | Ambulance, Fire Truck, Police | 🔴 Red     |
| MEDIUM   | Bus, Truck                    | 🟡 Yellow  |
| LOW      | Car, Motorcycle, Bicycle      | 🟢 Green   |
| NONE     | No vehicles detected          | ⚫ All OFF |

## 🎯 Controls

-   Press `q` in video window to quit
-   Click "Generate Excel" button to export detection log
-   Excel file includes: Timestamp, Vehicle Type, Priority

## 🔧 Troubleshooting

### Python script won't start

```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Can't connect to ESP32

1. Check IP address is correct
2. Ensure ESP32 and PC are on same WiFi network
3. Check Serial Monitor for ESP32 IP address

### LEDs not working

1. Check GPIO pin connections (12, 13, 15)
2. Verify LED polarity (long leg = +, short leg = -)
3. Check resistor values (220Ω recommended)
4. Test manually: http://192.168.1.50/led?color=red

### No vehicles detected

1. Ensure good lighting
2. Camera should face the road/traffic
3. First run downloads YOLO model (needs internet)
4. Try different video angles

## 📹 Getting Test Videos

You can use:

1. Your own traffic video recordings
2. Download from: https://pixabay.com/videos/search/traffic/
3. Use YouTube videos (with proper permissions)
4. Record from ESP32-CAM and save for testing

## 📊 Sample Output

Detection log Excel file contains:

```
Timestamp           | Vehicle Type | Priority
--------------------|--------------|----------
2024-11-04 10:30:15 | car         | LOW
2024-11-04 10:30:16 | truck       | MEDIUM
2024-11-04 10:30:20 | ambulance   | HIGH
```

## 🎓 Next Steps

1. Test with video file first
2. Then set up ESP32-CAM hardware
3. Connect LEDs and test LED control
4. Deploy for real-time traffic monitoring

## 💡 Tips

-   Use videos with clear vehicle visibility for best results
-   YOLOv8n is fast but less accurate; upgrade to yolov8m for better detection
-   Process every 2nd or 3rd frame for faster performance on slow PCs
-   Keep detection log under 10,000 entries for smooth Excel export
