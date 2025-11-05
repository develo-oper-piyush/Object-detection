import React from "react";
import { Car, AlertTriangle, TrendingUp, CreditCard } from "lucide-react";

const VehicleStats = ({ stats }) => {
    const statCards = [
        {
            title: "Total Detections",
            value: stats.totalDetections,
            icon: <Car size={24} />,
            color: "blue",
            trend: "+12%",
        },
        {
            title: "High Priority",
            value: stats.highPriority,
            icon: <AlertTriangle size={24} />,
            color: "red",
            trend: "+3",
        },
        {
            title: "Medium Priority",
            value: stats.mediumPriority,
            icon: <TrendingUp size={24} />,
            color: "orange",
            trend: "+18%",
        },
        {
            title: "Plates Detected",
            value: stats.withPlates,
            icon: <CreditCard size={24} />,
            color: "green",
            trend: `${Math.round(
                (stats.withPlates / stats.totalDetections) * 100
            )}%`,
        },
    ];

    return (
        <div className="stats-grid">
            {statCards.map((stat, index) => (
                <div key={index} className={`stat-card stat-${stat.color}`}>
                    <div className="stat-icon">{stat.icon}</div>
                    <div className="stat-content">
                        <p className="stat-label">{stat.title}</p>
                        <h2 className="stat-value">{stat.value}</h2>
                        <span className="stat-trend">{stat.trend}</span>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default VehicleStats;
