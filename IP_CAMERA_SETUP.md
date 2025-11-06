# IP Camera Setup Guide

## Using Your Phone as IP Camera

You can use your smartphone as an IP camera instead of ESP32-CAM. Here's how:

---

## 📱 Option 1: IP Webcam (Android) - RECOMMENDED

### Setup:

1. **Download App**: Install "IP Webcam" from Google Play Store
2. **Connect to WiFi**: Make sure your phone and computer are on the same WiFi network
3. **Start Server**:
    - Open the app
    - Scroll down and tap "Start server"
    - Note the IP address shown (e.g., `192.168.1.100:8080`)

### Usage:

```bash
# Replace with your phone's IP address
python new.py --ip http://192.168.1.100:8080/video

# With performance optimization
python new.py --ip http://192.168.1.100:8080/video --scale 0.75
```

### Features:

-   ✅ Best quality
-   ✅ Adjustable resolution
-   ✅ Night mode
-   ✅ Auto-focus
-   ✅ Zoom control

---

## 📱 Option 2: DroidCam (Android/iOS)

### Setup:

1. **Download App**: Install "DroidCam" from Play Store or App Store
2. **Connect to WiFi**: Same network as your computer
3. **Note IP Address**: The app shows the IP and port (default: 4747)

### Usage:

```bash
# Replace with your phone's IP
python new.py --ip http://192.168.1.100:4747/video
```

---

## 📱 Option 3: iVCam (iOS/Android)

### Setup:

1. **Download App**: Install "iVCam" from App Store or Play Store
2. **Install PC Client**: Download from https://www.e2esoft.com/ivcam/
3. **Connect**: Use USB or WiFi connection

### Usage:

```bash
# Usually accessed through the PC client, not direct URL
# Check app settings for stream URL
```

---

## 🌐 Option 4: Generic MJPEG Camera

For any IP camera that supports MJPEG streaming:

```bash
python new.py --ip http://CAMERA_IP:PORT/stream
```

Common ports: 8080, 8081, 8554

---

## 📹 Option 5: RTSP Camera

For professional IP cameras with RTSP support:

```bash
python new.py --ip rtsp://CAMERA_IP:554/stream

# With authentication
python new.py --ip rtsp://username:password@CAMERA_IP:554/stream
```

---

## 🔍 How to Find Your Phone's IP Address

### Method 1: Through the IP Camera App

-   Most apps display the IP address when server is running
-   Look for something like `http://192.168.1.100:8080`

### Method 2: WiFi Settings (Android)

1. Go to **Settings** → **WiFi**
2. Tap on connected network
3. Find **IP address**

### Method 3: WiFi Settings (iOS)

1. Go to **Settings** → **WiFi**
2. Tap the (i) icon next to connected network
3. Find **IP Address**

---

## 🚀 Complete Examples

### 1. IP Webcam (Best for Android)

```bash
python new.py --ip http://192.168.1.100:8080/video
```

### 2. DroidCam

```bash
python new.py --ip http://192.168.1.100:4747/video
```

### 3. ESP32-CAM (Original)

```bash
python new.py --ip 192.168.1.50
# or
python new.py --ip http://192.168.1.50/stream
```

### 4. With Lower Resolution (Faster)

```bash
python new.py --ip http://192.168.1.100:8080/video --scale 0.5
```

---

## ⚙️ Troubleshooting

### "Failed to open stream"

**Solutions:**

1. Check both devices are on same WiFi network
2. Verify IP address is correct
3. Make sure camera app is running
4. Try disabling firewall temporarily
5. Check the stream URL format

### Stream is laggy/slow

**Solutions:**

1. Lower the resolution in the camera app
2. Use `--scale 0.5` for faster processing
3. Move phone closer to WiFi router
4. Close other apps using camera

### "Connection refused"

**Solutions:**

1. Make sure camera app server is started
2. Check if port is correct (8080 for IP Webcam, 4747 for DroidCam)
3. Try accessing the URL in web browser first

### Poor detection quality

**Solutions:**

1. Increase resolution in camera app settings
2. Use `--scale 1.0` for full quality
3. Ensure good lighting
4. Position camera to capture vehicles clearly

---

## 📊 Recommended Settings

### For IP Webcam App:

-   **Resolution**: 1280x720 (720p) or 1920x1080 (1080p)
-   **Quality**: 80-90%
-   **FPS**: 30
-   **Video encoder**: MJPEG

### For Best Performance:

-   **Phone WiFi**: 5GHz band if available
-   **Camera position**: Stable mount, clear view of road
-   **Lighting**: Good daylight or artificial lighting
-   **Distance**: 3-10 meters from vehicles

---

## 🎯 Quick Start

1. **Install IP Camera App** on your phone
2. **Start the server** in the app
3. **Note the IP address** (e.g., 192.168.1.100:8080)
4. **Run detection**:
    ```bash
    python new.py --ip http://YOUR_PHONE_IP:8080/video
    ```
5. **Position your phone** to capture vehicle traffic
6. **Watch the detection** in the OpenCV window
7. **Press 'e'** to export data to Excel
8. **Press 'q'** to quit

---

## 💡 Pro Tips

1. **Use a phone stand** for stable video
2. **Keep phone plugged in** for long sessions
3. **Enable "Keep screen on"** in camera app
4. **Use portrait orientation** for better road coverage
5. **Test stream in browser** first: Open `http://PHONE_IP:8080` in Chrome
6. **Adjust phone camera settings** for best lighting
7. **Position camera higher** for better vehicle tracking

---

## 🔗 Useful Links

-   IP Webcam: https://play.google.com/store/apps/details?id=com.pas.webcam
-   DroidCam: https://www.dev47apps.com/
-   iVCam: https://www.e2esoft.com/ivcam/

Enjoy real-time vehicle detection with your phone camera! 📱🚗
