# 🎯 Quick Command Reference

## 📖 Getting Help

```bash
# Display all available options and usage examples
python new.py --help
```

**What it shows:**

-   Complete list of all command-line flags
-   Description of each option
-   Default values and valid ranges
-   Usage examples for common scenarios
-   Supported camera sources and formats

---

## Vehicle Detection Mode (Default)

```bash
# Basic vehicle detection
python new.py --video traffic.mp4

# With pedestrian detection
python new.py --video traffic.mp4 --pedestrians

# From IP camera
python new.py --ip http://192.168.1.100:8080/video

# From ESP32-CAM
python new.py --ip 192.168.1.50
```

## General Object Detection Mode (80+ Classes)

```bash
# Basic general object detection
python new.py --video scene.mp4 --general-objects

# With pedestrian highlighting
python new.py --video scene.mp4 --general-objects --pedestrians

# From IP camera
python new.py --ip http://192.168.1.100:8080/video --general-objects

# From ESP32-CAM
python new.py --ip 192.168.1.50 --general-objects
```

## Performance Modes

```bash
# Fast (50% resolution, 40-50 FPS)
python new.py --video FILE --general-objects --scale 0.5

# Balanced (75% resolution, 30-40 FPS) - DEFAULT
python new.py --video FILE --general-objects --scale 0.75

# Best Quality (100% resolution, 15-20 FPS)
python new.py --video FILE --general-objects --scale 1.0
```

## Keyboard Controls

-   **q** or **ESC**: Quit
-   **e**: Export to Excel

## 80 Detectable Object Classes

**People & Animals:** person, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe

**Vehicles:** bicycle, car, motorcycle, airplane, bus, train, truck, boat

**Furniture:** chair, couch, potted plant, bed, dining table, toilet

**Electronics:** tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator

**Food:** bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake

**Sports:** frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket

**Accessories:** backpack, umbrella, handbag, tie, suitcase, book, clock, vase, scissors, teddy bear, hair drier, toothbrush

**Outdoor:** traffic light, fire hydrant, stop sign, parking meter, bench
