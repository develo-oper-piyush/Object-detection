# 🎯 Web Dashboard Setup Guide

## ✅ What Was Created

A complete React-based web dashboard with:

-   ⚛️ React 18 + Vite (latest)
-   🎨 Modern dark theme UI
-   📊 Real-time statistics display
-   📋 Detection history table
-   📈 Priority distribution charts
-   📹 Live feed placeholder
-   📱 Fully responsive design

## 📁 Files Created

```
Web-Dashboard/
├── package.json              # Dependencies & scripts
├── vite.config.js           # Vite configuration
├── index.html               # HTML entry point
├── .gitignore              # Git ignore rules
├── README.md               # Dashboard documentation
└── src/
    ├── main.jsx            # React entry point
    ├── App.jsx             # Root component (imports Dashboard)
    ├── App.css             # Main styling (complete)
    ├── index.css           # Global CSS variables
    └── components/
        ├── Dashboard.jsx           # Main dashboard (✅)
        ├── VehicleStats.jsx        # Stats cards (✅)
        ├── RecentDetections.jsx    # Detections table (✅)
        ├── PriorityChart.jsx       # Priority chart (✅)
        └── LiveFeed.jsx            # Camera feed (✅)
```

## 🚀 How to Run

### Step 1: Open PowerShell as Administrator

Right-click PowerShell → "Run as Administrator"

### Step 2: Enable Script Execution (One-time)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Press `Y` to confirm.

### Step 3: Navigate to Dashboard Folder

```cmd
cd "c:\Users\Piyush Chaudhary\OneDrive\Desktop\Object-detection\Web-Dashboard"
```

### Step 4: Install Dependencies

```cmd
npm install
```

This will install:

-   React 18
-   React DOM
-   Vite (build tool)
-   Lucide React (icons)
-   Recharts (charts library)

### Step 5: Start Development Server

```cmd
npm run dev
```

### Step 6: Open in Browser

The terminal will show:

```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

Open your browser to: **http://localhost:3000**

## 🎨 What You'll See

### Dashboard Header

-   🚗 Vehicle Detection Dashboard logo
-   🟢 Connection status indicator
-   🔄 Refresh button
-   📊 Export button

### Statistics Cards (4 Cards)

1. **Total Detections** - Blue card with car icon
2. **High Priority** - Red card with alert icon
3. **Medium Priority** - Orange card with trending icon
4. **Plates Detected** - Green card with card icon

### Priority Chart

Horizontal bar chart showing:

-   🔴 High Priority (red)
-   🟠 Medium Priority (orange)
-   🟢 Low Priority (green)

### Recent Detections Table

Columns:

-   ⏰ Time
-   🚗 Vehicle (with emoji)
-   🏷️ Priority (colored badge)
-   🔢 License Plate (code format)
-   📊 Confidence (progress bar)

### Live Feed

Camera feed placeholder with:

-   Detection boxes overlay
-   Video info (resolution, FPS)
-   Connection status

---

## 🔧 Customization

### Change Port

Edit `vite.config.js`:

```javascript
server: {
  port: 5173, // Change to your preferred port
}
```

### Change Colors

Edit `src/index.css`:

```css
:root {
    --primary-color: #your-color;
    --dark-bg: #your-bg;
}
```

### Add Real Data

Edit `src/components/Dashboard.jsx`:

```javascript
useEffect(() => {
    // Replace mockData with actual API call
    fetch("/api/detections")
        .then((res) => res.json())
        .then((data) => setRecentDetections(data));
}, []);
```

---

## 📦 Build for Production

```cmd
npm run build
```

This creates a `dist/` folder with optimized files.

---

## 🐛 Troubleshooting

### Problem: "npm not found"

**Solution:** Install Node.js from https://nodejs.org/

### Problem: "Cannot find module"

**Solution:**

```cmd
rm -rf node_modules
npm install
```

### Problem: Port already in use

**Solution:** Change port in `vite.config.js` or kill process:

```cmd
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

### Problem: "Access denied" error

**Solution:** Run PowerShell as Administrator

---

## 🎯 Component Breakdown

### Dashboard.jsx

-   Main container component
-   Manages state (stats, detections, connection status)
-   Imports all child components
-   Handles refresh and export

### VehicleStats.jsx

-   Displays 4 stat cards
-   Props: `stats` object
-   Auto-calculates trends

### RecentDetections.jsx

-   Table of recent detections
-   Props: `detections` array
-   Vehicle emoji icons
-   Priority badges
-   Confidence bars

### PriorityChart.jsx

-   Horizontal bar chart
-   Props: `stats` object
-   Shows HIGH/MEDIUM/LOW distribution
-   Summary statistics

### LiveFeed.jsx

-   Camera feed placeholder
-   Props: `isConnected` boolean
-   Detection boxes overlay
-   Video info display

---

## 🔌 Next: Connect to Python Backend

Create a Flask API in your Python project:

```python
# api.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'totalDetections': 147,
        'highPriority': 12,
        'mediumPriority': 45,
        'lowPriority': 90,
        'withPlates': 98,
        'withoutPlates': 49
    })

@app.route('/api/detections')
def get_detections():
    # Return recent detections from your log
    return jsonify([...])

if __name__ == '__main__':
    app.run(port=5000)
```

Then update Dashboard.jsx to fetch from these endpoints!

---

## ✅ Success Checklist

-   [ ] PowerShell execution policy set
-   [ ] Node.js installed (check with `node --version`)
-   [ ] Navigated to Web-Dashboard folder
-   [ ] Ran `npm install` successfully
-   [ ] Ran `npm run dev` successfully
-   [ ] Browser opens to http://localhost:3000
-   [ ] Dashboard displays with all components
-   [ ] Can see stats cards, chart, table, and live feed

---

**Your web dashboard is ready!** 🎉

Run `npm run dev` and visit http://localhost:3000 to see it in action!
