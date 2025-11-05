import React from "react";

const RecentDetections = ({ detections }) => {
    const getPriorityBadge = (priority) => {
        const badges = {
            HIGH: "badge-high",
            MEDIUM: "badge-medium",
            LOW: "badge-low",
        };
        return badges[priority] || "badge-low";
    };

    const getVehicleIcon = (vehicle) => {
        const icons = {
            car: "🚗",
            truck: "🚚",
            bus: "🚌",
            ambulance: "🚑",
            motorcycle: "🏍️",
            bicycle: "🚲",
        };
        return icons[vehicle.toLowerCase()] || "🚗";
    };

    return (
        <div className="detections-list">
            {detections.length === 0 ? (
                <div className="empty-state">
                    <p>No detections yet</p>
                </div>
            ) : (
                <table className="detections-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Vehicle</th>
                            <th>Priority</th>
                            <th>License Plate</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
                        {detections.map((detection) => (
                            <tr key={detection.id}>
                                <td className="time-cell">
                                    {detection.timestamp.split(" ")[1]}
                                </td>
                                <td className="vehicle-cell">
                                    <span className="vehicle-icon">
                                        {getVehicleIcon(detection.vehicle)}
                                    </span>
                                    {detection.vehicle}
                                </td>
                                <td>
                                    <span
                                        className={`badge ${getPriorityBadge(
                                            detection.priority
                                        )}`}
                                    >
                                        {detection.priority}
                                    </span>
                                </td>
                                <td className="plate-cell">
                                    <code>{detection.plate}</code>
                                </td>
                                <td className="confidence-cell">
                                    <div className="confidence-bar">
                                        <div
                                            className="confidence-fill"
                                            style={{
                                                width: `${
                                                    detection.confidence * 100
                                                }%`,
                                            }}
                                        ></div>
                                        <span className="confidence-text">
                                            {(
                                                detection.confidence * 100
                                            ).toFixed(0)}
                                            %
                                        </span>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default RecentDetections;
