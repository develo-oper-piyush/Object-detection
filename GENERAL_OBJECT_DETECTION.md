# 🎯 General Object Detection Mode - Complete Guide

## 📋 Overview

The system now supports **TWO detection modes**:

### 1️⃣ **Vehicle Mode** (Default)

-   Specialized for traffic management
-   Detects: cars, trucks, buses, motorcycles, bicycles
-   Features: Priority classification, license plate OCR, LED control
-   Use cases: Traffic monitoring, parking, toll booths

### 2️⃣ **General Object Mode** (NEW! 🎉)

-   Detects 80+ everyday objects from COCO dataset
-   Features: Multi-class detection, object counting, color-coded boxes
-   Use cases: Retail, security, home monitoring, research

---

## 🚀 Quick Start

### Vehicle Mode (Default)

```bash
python new.py --video traffic.mp4
```

### General Object Mode (NEW!)

```bash
python new.py --video scene.mp4 --general-objects
```

---

## 📦 What Objects Can Be Detected?

The YOLO model is pre-trained on **80 object classes** from the COCO dataset:

### 👥 People & Animals (16 classes)

-   person, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe

### 🚗 Vehicles (8 classes)

-   bicycle, car, motorcycle, airplane, bus, train, truck, boat

### 🪑 Furniture & Appliances (13 classes)

-   chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator

### 🍎 Food & Drink (11 classes)

-   bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

### ⚽ Sports & Recreation (10 classes)

-   frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket

### 🎒 Accessories & Items (15 classes)

-   backpack, umbrella, handbag, tie, suitcase, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

### 🚦 Outdoor & Traffic (7 classes)

-   traffic light, fire hydrant, stop sign, parking meter, bench

**Total: 80 classes** that work out of the box - no training required!

---

## 💡 Command Examples

### Basic Commands

```bash
# Vehicle detection (default)
python new.py --video traffic.mp4

# General object detection
python new.py --video scene.mp4 --general-objects

# General objects from IP camera
python new.py --ip http://192.168.1.100:8080/video --general-objects

# General objects from ESP32-CAM
python new.py --ip 192.168.1.50 --general-objects
```

### With Pedestrian Tracking

```bash
# Vehicle mode with pedestrian detection
python new.py --video traffic.mp4 --pedestrians

# General mode with pedestrian highlighting
python new.py --video scene.mp4 --general-objects --pedestrians
```

### Performance Optimization

```bash
# Fast mode (50% resolution, 40-50 FPS)
python new.py --video scene.mp4 --general-objects --scale 0.5

# Balanced mode (75% resolution, 30-40 FPS) - DEFAULT
python new.py --video scene.mp4 --general-objects --scale 0.75

# Best quality (100% resolution, 15-20 FPS)
python new.py --video scene.mp4 --general-objects --scale 1.0
```

---

## 🎨 Visual Features

### General Object Mode Display:

```
┌─────────────────────────────────────────────┐
│  General Object Detection (80+ Classes)    │
├─────────────────────────────────────────────┤
│                                             │
│  [Person 0.95]   [Dog 0.88]   [Chair 0.92] │
│  [Laptop 0.91]   [Cup 0.87]                │
│                                             │
│  Status Bar:                                │
│  Total Objects: 15 | Unique Classes: 7     │
│                                             │
│  Top Detected:                              │
│  • person: 3                                │
│  • chair: 4                                 │
│  • laptop: 2                                │
│  • cup: 3                                   │
│  • bottle: 2                                │
│                                             │
└─────────────────────────────────────────────┘
```

**Features:**

-   ✅ Each object class has a unique color
-   ✅ Confidence scores displayed
-   ✅ Real-time object counting
-   ✅ Top 5 detected objects shown
-   ✅ Total object count in status bar

---

## 📊 Excel Export

### Vehicle Mode Export Format:

| Timestamp           | Vehicle Type | Priority | License Plate | Pedestrians |
| ------------------- | ------------ | -------- | ------------- | ----------- |
| 2025-11-06 14:30:15 | car          | LOW      | ABC1234       | 2           |

### General Object Mode Export Format:

| Timestamp           | Object Type | Priority | License Plate | Pedestrians |
| ------------------- | ----------- | -------- | ------------- | ----------- |
| 2025-11-06 14:30:15 | person      | N/A      | N/A           | 0           |
| 2025-11-06 14:30:16 | dog         | N/A      | N/A           | 0           |
| 2025-11-06 14:30:17 | laptop      | N/A      | N/A           | 0           |

**Press 'e' key** during detection to export data to Excel!

---

## 🔧 Technical Details

### How It Works

1. **YOLOv8n Model**: Pre-trained on COCO dataset (80 classes)
2. **Detection Mode Switch**: `--general-objects` flag enables general mode
3. **No Retraining Needed**: Model already knows all 80 classes!
4. **Same Performance**: 30-40 FPS regardless of mode

### Code Architecture

```python
# Vehicle Mode (default)
detector = ESP32CamDetector(
    video_path="traffic.mp4",
    general_mode=False  # Default
)

# General Object Mode
detector = ESP32CamDetector(
    video_path="scene.mp4",
    general_mode=True  # Enable general detection
)
```

### Detection Logic

**Vehicle Mode:**

-   Filters detections to vehicles only
-   Applies priority classification
-   Runs license plate OCR
-   Controls ESP32 LEDs

**General Mode:**

-   Detects ALL 80 COCO classes
-   Color-codes each class
-   Counts objects by type
-   No priority/OCR (not applicable)

---

## 🎯 Use Cases

### Vehicle Mode Use Cases:

-   🚦 Traffic management and signal control
-   🅿️ Parking lot monitoring
-   💰 Automated toll collection
-   🚓 Emergency vehicle detection

### General Object Mode Use Cases:

#### 🏪 Retail Analytics

```bash
# Detect customers, products, shopping carts
python new.py --ip STORE_CAMERA_IP --general-objects
```

-   Track customer flow
-   Monitor queue lengths (count persons)
-   Detect shelf inventory (bottles, packages)
-   Security monitoring

#### 🏠 Home Security

```bash
# Detect people, pets, packages
python new.py --ip HOME_CAMERA_IP --general-objects --pedestrians
```

-   Intruder detection (person)
-   Package delivery monitoring (backpack, suitcase)
-   Pet monitoring (dog, cat)
-   Activity detection

#### 🏢 Office Monitoring

```bash
# Track workspace usage
python new.py --video office.mp4 --general-objects
```

-   Desk occupancy (person + chair + laptop)
-   Meeting room usage (person count)
-   Equipment tracking (laptop, mouse, keyboard)
-   Safety compliance

#### 🌳 Wildlife Research

```bash
# Detect animals in nature
python new.py --video wildlife.mp4 --general-objects
```

-   Animal counting (bird, dog, horse, elephant, bear, etc.)
-   Behavior analysis
-   Population monitoring
-   Habitat study

#### 🍽️ Restaurant Management

```bash
# Monitor dining area
python new.py --ip RESTAURANT_CAMERA_IP --general-objects
```

-   Table occupancy (person + chair)
-   Wait time estimation
-   Food delivery tracking (bowl, cup, bottle)
-   Cleaning needs detection

---

## ⌨️ Keyboard Controls

Same for both modes:

| Key   | Action             |
| ----- | ------------------ |
| `q`   | Quit application   |
| `e`   | Export to Excel    |
| `ESC` | Quit (alternative) |

---

## 📈 Performance Tips

### For General Object Mode:

1. **Many Objects (>20 per frame)**

    ```bash
    # Use lower resolution for speed
    python new.py --video busy_scene.mp4 --general-objects --scale 0.5
    ```

2. **Few Objects (<10 per frame)**

    ```bash
    # Use higher resolution for accuracy
    python new.py --video simple_scene.mp4 --general-objects --scale 1.0
    ```

3. **Real-time Live Monitoring**
    ```bash
    # Balance speed and quality
    python new.py --ip CAMERA_IP --general-objects --scale 0.75
    ```

---

## 🔄 Comparison: Vehicle vs General Mode

| Feature                 | Vehicle Mode        | General Mode         |
| ----------------------- | ------------------- | -------------------- |
| **Object Classes**      | 7 (vehicles only)   | 80 (all COCO)        |
| **Priority System**     | ✅ HIGH/MED/LOW     | ❌ Not applicable    |
| **License Plate OCR**   | ✅ Yes (EasyOCR)    | ❌ No                |
| **LED Control**         | ✅ Yes (ESP32)      | ❌ No                |
| **Object Counting**     | ❌ No               | ✅ Yes, by class     |
| **Color Coding**        | By priority (R/Y/G) | By class (80 colors) |
| **Pedestrian Tracking** | ✅ Optional         | ✅ Optional          |
| **Excel Export**        | ✅ Yes              | ✅ Yes               |
| **Performance**         | 30-40 FPS           | 30-40 FPS            |
| **Use Cases**           | Traffic only        | Universal            |

---

## 🎓 Examples by Industry

### Education & Research

```bash
# Lab object tracking
python new.py --video lab.mp4 --general-objects
# Detects: person, laptop, mouse, keyboard, book, chair, bottle
```

### Healthcare

```bash
# Hospital monitoring
python new.py --ip HOSPITAL_CAM --general-objects
# Detects: person, bed, chair, laptop, cell phone
```

### Agriculture

```bash
# Farm monitoring
python new.py --video farm.mp4 --general-objects
# Detects: person, horse, cow, sheep, dog, truck
```

### Construction

```bash
# Site monitoring
python new.py --ip SITE_CAM --general-objects --pedestrians
# Detects: person, truck, car, chair, laptop (office trailer)
```

---

## ❓ FAQs

### Q: Do I need to train a model for general object detection?

**A:** No! The YOLOv8n model is already pre-trained on 80 object classes. Just add the `--general-objects` flag.

### Q: Can I detect custom objects not in the 80 classes?

**A:** You would need to train a custom YOLO model. The current implementation uses the pre-trained COCO model.

### Q: Which mode is faster?

**A:** Both modes have similar performance (30-40 FPS). General mode might be slightly slower if many objects are detected.

### Q: Can I use both modes simultaneously?

**A:** No, you choose one mode per session. Use `--general-objects` for general mode, or omit it for vehicle mode.

### Q: Does general mode support license plate reading?

**A:** No, license plate OCR is only available in vehicle mode as it's specific to vehicle applications.

### Q: Can I use ESP32-CAM LED control in general mode?

**A:** No, LED control is tied to vehicle priority system (HIGH/MEDIUM/LOW), which only exists in vehicle mode.

---

## 🚀 Next Steps

1. **Try General Mode:**

    ```bash
    python new.py --video YOUR_VIDEO.mp4 --general-objects
    ```

2. **Test with Webcam:**

    ```bash
    # Use IP Webcam app on phone
    python new.py --ip http://YOUR_PHONE_IP:8080/video --general-objects
    ```

3. **Optimize for Your Use Case:**

    - Retail: Use --scale 0.75 for balanced performance
    - Security: Use --scale 0.5 for real-time speed
    - Research: Use --scale 1.0 for best accuracy

4. **Export and Analyze:**
    - Press 'e' during detection
    - Open the Excel file to analyze object counts
    - Use for reports, statistics, insights

---

## 📞 Support

-   **GitHub Issues**: Report bugs or request features
-   **Documentation**: Check README.md for full system guide
-   **Examples**: See usage examples above

---

**Happy Detecting! 🎉**

Detect vehicles, people, animals, objects, and more with a single command!
