import React, { useState, useEffect } from "react";
import DotGrid from "../components/ui/DotGrid";
import {
    Car,
    Truck,
    Bus,
    Bike,
    AlertTriangle,
    Activity,
    Eye,
    FileSpreadsheet,
    RefreshCw,
    TrendingUp,
} from "lucide-react";
import VehicleStats from "./VehicleStats";
import RecentDetections from "./RecentDetections";
import PriorityChart from "./PriorityChart";
import LiveFeed from "./LiveFeed";

const Dashboard = () => {
    const [stats, setStats] = useState({
        totalDetections: 0,
        highPriority: 0,
        mediumPriority: 0,
        lowPriority: 0,
        withPlates: 0,
        withoutPlates: 0,
    });

    const [recentDetections, setRecentDetections] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [lastUpdate, setLastUpdate] = useState(null);

    // Simulate real-time data updates (replace with actual API calls)
    useEffect(() => {
        // Simulated data - replace with actual fetch from your Python backend
        const mockData = {
            totalDetections: 147,
            highPriority: 12,
            mediumPriority: 45,
            lowPriority: 90,
            withPlates: 98,
            withoutPlates: 49,
        };

        const mockDetections = [
            {
                id: 1,
                timestamp: "2025-11-05 14:30:15",
                vehicle: "car",
                priority: "LOW",
                plate: "ABC1234",
                confidence: 0.85,
            },
            {
                id: 2,
                timestamp: "2025-11-05 14:30:18",
                vehicle: "truck",
                priority: "MEDIUM",
                plate: "XYZ9876",
                confidence: 0.92,
            },
            {
                id: 3,
                timestamp: "2025-11-05 14:30:22",
                vehicle: "ambulance",
                priority: "HIGH",
                plate: "EMG911",
                confidence: 0.88,
            },
            {
                id: 4,
                timestamp: "2025-11-05 14:30:25",
                vehicle: "bus",
                priority: "MEDIUM",
                plate: "BUS456",
                confidence: 0.79,
            },
            {
                id: 5,
                timestamp: "2025-11-05 14:30:28",
                vehicle: "motorcycle",
                priority: "LOW",
                plate: "N/A",
                confidence: 0.91,
            },
        ];

        setStats(mockData);
        setRecentDetections(mockDetections);
        setIsConnected(true);
        setLastUpdate(new Date());

        // Simulate periodic updates
        const interval = setInterval(() => {
            setLastUpdate(new Date());
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    const handleRefresh = () => {
        // Implement actual data refresh
        setLastUpdate(new Date());
    };

    const handleExport = () => {
        // Export Excel file and open in new tab
        // Assuming your Python backend has an endpoint that serves the Excel file
        const exportUrl = "http://localhost:5000/api/export"; // Update with your actual backend URL

        // Option 1: If backend returns file path, open it directly
        window.open(exportUrl, "_blank");

        // Option 2: If you need to fetch and download
        // fetch(exportUrl)
        //     .then(response => response.blob())
        //     .then(blob => {
        //         const url = window.URL.createObjectURL(blob);
        //         window.open(url, '_blank');
        //     })
        //     .catch(error => {
        //         console.error('Export failed:', error);
        //         alert('Failed to export data. Please try again.');
        //     });
    };

    return (
        <div className="dashboard">
            {/* Header */}
            <header className="dashboard-header">
                <div className="header-content">
                    <div className="header-left">
                        <Car className="header-icon" size={32} />
                        <div>
                            <h1>Vehicle Detection Dashboard</h1>
                            <p className="subtitle">
                                Real-time monitoring & license plate recognition
                            </p>
                        </div>
                    </div>
                    <div className="header-right">
                        <div className="status-indicator">
                            <div
                                className={`status-dot ${
                                    isConnected ? "connected" : "disconnected"
                                }`}
                            ></div>
                            <span>
                                {isConnected ? "Connected" : "Disconnected"}
                            </span>
                        </div>
                        <button
                            className="btn btn-secondary"
                            onClick={handleRefresh}
                        >
                            <RefreshCw size={18} />
                            Refresh
                        </button>
                        <button
                            className="btn btn-primary"
                            onClick={handleExport}
                        >
                            <FileSpreadsheet size={18} />
                            Export
                        </button>
                    </div>
                </div>
            </header>

            {/* Background DotGrid */}
            <DotGrid
                dotSize={5}
                gap={15}
                baseColor="#3d3055"
                activeColor="#52ffff"
                proximity={120}
                shockRadius={250}
                shockStrength={5}
                resistance={750}
                returnDuration={1.5}
            />

            {/* Main Content */}
            <div className="dashboard-content">
                {/* Stats Grid */}
                <VehicleStats stats={stats} />

                {/* Charts and Data */}
                <div className="dashboard-grid">
                    {/* Priority Distribution Chart */}
                    <div className="card chart-card">
                        <div className="card-header">
                            <h3>Priority Distribution</h3>
                            <TrendingUp size={20} className="card-icon" />
                        </div>
                        <PriorityChart stats={stats} />
                    </div>

                    {/* Recent Detections */}
                    <div className="card detections-card">
                        <div className="card-header">
                            <h3>Recent Detections</h3>
                            <Activity size={20} className="card-icon" />
                        </div>
                        <RecentDetections detections={recentDetections} />
                    </div>
                </div>

                {/* Live Feed */}
                <LiveFeed isConnected={isConnected} />
            </div>

            {/* Footer */}
            <footer className="dashboard-footer">
                <p>
                    Last updated:{" "}
                    {lastUpdate ? lastUpdate.toLocaleString() : "Never"}
                </p>
                <p>© 2025 Vehicle Detection System | LPR Enabled</p>
            </footer>
        </div>
    );
};

export default Dashboard;
