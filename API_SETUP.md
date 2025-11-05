# API Setup Guide

## Overview

This Flask API serves as the backend for the Vehicle Detection Dashboard, providing endpoints to export Excel files and fetch detection data.

## Installation

1. **Install Flask dependencies:**

    ```bash
    pip install flask flask-cors
    ```

    Or install all dependencies from requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

## Running the API

1. **Start the Flask server:**

    ```bash
    python api.py
    ```

2. **The API will be available at:**
    ```
    http://localhost:5000
    ```

## API Endpoints

### 1. Export Excel File (Open in Browser)

-   **URL:** `http://localhost:5000/api/export`
-   **Method:** GET
-   **Description:** Opens the most recent Excel file in a new browser tab
-   **Response:** Excel file

### 2. Download Excel File

-   **URL:** `http://localhost:5000/api/export/download`
-   **Method:** GET
-   **Description:** Downloads the most recent Excel file
-   **Response:** Excel file (as attachment)

### 3. Get Statistics

-   **URL:** `http://localhost:5000/api/stats`
-   **Method:** GET
-   **Description:** Get detection statistics (placeholder)
-   **Response:**
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

### 4. Get Recent Detections

-   **URL:** `http://localhost:5000/api/detections`
-   **Method:** GET
-   **Description:** Get recent vehicle detections (placeholder)
-   **Response:** Array of detection objects

### 5. Health Check

-   **URL:** `http://localhost:5000/api/health`
-   **Method:** GET
-   **Description:** Check if API is running
-   **Response:**
    ```json
    {
        "status": "ok",
        "message": "API is running"
    }
    ```

## Integration with Dashboard

The React dashboard is already configured to use this API:

1. **Export Button:** Clicking "Export" opens the Excel file at `http://localhost:5000/api/export`
2. **Vite Proxy:** The dashboard's `vite.config.js` proxies `/api/*` requests to `localhost:5000`

## Usage Flow

1. **Run the detection system** (`new.py`) to generate Excel files:

    ```bash
    python new.py --video traffic.mp4
    ```

2. **Start the API server:**

    ```bash
    python api.py
    ```

3. **Start the dashboard** (in Web-Dashboard folder):

    ```bash
    cd Web-Dashboard/Web-Dashboard
    npm run dev
    ```

4. **Click Export button** in the dashboard to open the generated Excel file in a new tab

## Notes

-   The API looks for Excel files matching the pattern `vehicle_detections_*.xlsx`
-   It automatically serves the most recent file based on creation time
-   CORS is enabled to allow requests from the React frontend
-   The Excel file opens in the browser instead of downloading (can be changed to download if needed)

## Troubleshooting

**Issue:** "No Excel file found"

-   **Solution:** Run `new.py` to generate detections first, then press 'e' to export Excel

**Issue:** CORS errors

-   **Solution:** Make sure `flask-cors` is installed and CORS(app) is enabled in `api.py`

**Issue:** Port 5000 already in use

-   **Solution:** Change the port in `api.py` (line: `app.run(port=5000)`) and update the dashboard's `handleExport` function
