# ESP32-CAM LED Wiring Diagram

## Component List

1. ESP32-CAM (AI-Thinker) - 1x
2. Red LED (5mm) - 1x
3. Yellow LED (5mm) - 1x
4. Green LED (5mm) - 1x
5. 220Ω Resistors - 3x
6. Breadboard (optional)
7. Jumper wires

## Pin Connections

### Red LED (High Priority Indicator)

```
ESP32-CAM GPIO 12 ─────[220Ω]─────┐
                                  │
                               LED(+) Red LED
                                  │
                               LED(-)
                                  │
                                 GND
```

### Yellow LED (Medium Priority Indicator)

```
ESP32-CAM GPIO 13 ─────[220Ω]─────┐
                                  │
                               LED(+) Yellow LED
                                  │
                               LED(-)
                                  │
                                 GND
```

### Green LED (Low Priority Indicator)

```
ESP32-CAM GPIO 15 ─────[220Ω]─────┐
                                  │
                               LED(+) Green LED
                                  │
                               LED(-)
                                  │
                                 GND
```

## Complete Wiring Schematic

```
                    ESP32-CAM
                 ┌──────────────┐
                 │              │
                 │         GND  ├─────────────┬──────────┬─────────┐
                 │              │             │          │         │
                 │      GPIO 12 ├─[220Ω]──[Red LED]─────┘          │
                 │              │                                  │
                 │      GPIO 13 ├─[220Ω]──[Yellow LED]────────────┘
                 │              │
                 │      GPIO 15 ├─[220Ω]──[Green LED]
                 │              │
                 │          5V  ├─── Power Supply (+5V)
                 │              │
                 └──────────────┘
```

## LED Identification

### How to identify LED polarity:

-   **Long leg** = Anode (+) = connects to GPIO through resistor
-   **Short leg** = Cathode (-) = connects to GND
-   **Flat edge** on LED body = Cathode (-) side

```
     Long leg (+)
         │
         │
    ┌────┴────┐
    │   LED   │  ← Round side
    │    ⌒    │
    └────┬────┘
         │         Flat edge → Cathode (-)
    Short leg (-)
```

## Step-by-Step Wiring Instructions

### 1. Prepare Components

-   [ ] Gather all LEDs, resistors, and wires
-   [ ] Identify LED polarity (long leg = +)
-   [ ] Have breadboard ready (optional but recommended)

### 2. Connect Red LED (HIGH Priority)

-   [ ] Insert 220Ω resistor into breadboard
-   [ ] Connect one resistor end to GPIO 12
-   [ ] Connect other resistor end to Red LED long leg (+)
-   [ ] Connect Red LED short leg (-) to GND

### 3. Connect Yellow LED (MEDIUM Priority)

-   [ ] Insert 220Ω resistor into breadboard
-   [ ] Connect one resistor end to GPIO 13
-   [ ] Connect other resistor end to Yellow LED long leg (+)
-   [ ] Connect Yellow LED short leg (-) to GND

### 4. Connect Green LED (LOW Priority)

-   [ ] Insert 220Ω resistor into breadboard
-   [ ] Connect one resistor end to GPIO 15
-   [ ] Connect other resistor end to Green LED long leg (+)
-   [ ] Connect Green LED short leg (-) to GND

### 5. Power Connections

-   [ ] Connect ESP32-CAM GND to breadboard ground rail
-   [ ] Connect ESP32-CAM 5V to power supply
-   [ ] Ensure all LED cathodes connect to common ground

## GPIO Pin Map (AI-Thinker ESP32-CAM)

```
                                 ┌─────┐
                                 │ ANT │
                                 └─────┘
                    ┌────────────────────────────┐
                    │                            │
              IO12  ○  Red LED                   │  Camera
              IO13  ○  Yellow LED                │  Connector
              IO15  ○  Green LED                 │
               GND  ○                            │
                    │                            │
                    │         ESP32-CAM          │
                    │      (AI-Thinker)          │
                    │                            │
               5V   ○                            │
              GND   ○                            │
                    │                            │
                    └────────────────────────────┘
                            │      │
                         ┌──┴──┐ ┌┴──┐
                         │ USB │ │uSD│
                         └─────┘ └───┘
```

## Important Notes

⚠️ **DO NOT** connect LEDs directly to GPIO pins without resistors!

-   This can damage the ESP32 or LEDs
-   Always use current-limiting resistors (220Ω recommended)

⚠️ **LED Polarity Matters**

-   Reverse polarity = LED won't light up
-   Double-check before powering on

⚠️ **Power Supply**

-   ESP32-CAM needs stable 5V supply
-   USB power may be insufficient when camera is active
-   Use external 5V power adapter (≥ 2A recommended)

⚠️ **GPIO Limitations**

-   Some GPIOs are used by camera
-   Don't use camera pins for LEDs
-   GPIO 12, 13, 15 are safe for LEDs

## Testing LED Connections

After wiring, test each LED manually:

### Via Web Browser:

```
http://192.168.1.50/led?color=red      # Test Red LED
http://192.168.1.50/led?color=yellow   # Test Yellow LED
http://192.168.1.50/led?color=green    # Test Green LED
http://192.168.1.50/led?color=off      # Turn all off
```

### Via Serial Monitor:

Upload the code and watch for LED status messages:

-   "LED: RED (High Priority)"
-   "LED: YELLOW (Medium Priority)"
-   "LED: GREEN (Low Priority)"
-   "LED: OFF (No vehicles)"

## Troubleshooting LED Issues

### LED doesn't light up:

1. Check polarity (long leg to resistor, short leg to GND)
2. Verify resistor connection
3. Test with multimeter
4. Try different LED (might be dead)

### LED always on or always off:

1. Check GPIO pin number in code
2. Verify wiring matches code (GPIO 12/13/15)
3. Re-upload Arduino sketch

### Dim LED:

1. Check resistor value (220Ω is good)
2. Verify power supply voltage (should be 5V)
3. Check for loose connections

### Wrong color lights up:

1. Verify GPIO pin assignments
2. Double-check color wiring
3. Re-check code configuration

## Alternative Wiring (Common Anode)

If using common anode RGB LED or LED modules:

```
                     +5V
                      │
              ┌───────┼───────┬───────┐
              │       │       │       │
           [LED R] [LED Y] [LED G]    │
              │       │       │       │
          [220Ω]  [220Ω]  [220Ω]      │
              │       │       │       │
           GPIO12  GPIO13  GPIO15     │
                                      │
                   ESP32-CAM          │
```

## Safety Checklist

-   [ ] Power off before wiring
-   [ ] Double-check polarity
-   [ ] Verify resistor values
-   [ ] Check for short circuits
-   [ ] Secure all connections
-   [ ] Test one LED at a time
-   [ ] Monitor ESP32 temperature during operation

## Recommended Layout

For best visibility, arrange LEDs in a traffic light pattern:

```
    ┌─────┐
    │ 🔴  │  ← Red (Top) = HIGH Priority
    ├─────┤
    │ 🟡  │  ← Yellow (Middle) = MEDIUM Priority
    ├─────┤
    │ 🟢  │  ← Green (Bottom) = LOW Priority
    └─────┘
```
