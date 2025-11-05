import React from "react";

const PriorityChart = ({ stats }) => {
    const total = stats.highPriority + stats.mediumPriority + stats.lowPriority;

    const chartData = [
        {
            label: "High",
            value: stats.highPriority,
            percentage:
                total > 0 ? ((stats.highPriority / total) * 100).toFixed(1) : 0,
            color: "#ef4444",
        },
        {
            label: "Medium",
            value: stats.mediumPriority,
            percentage:
                total > 0
                    ? ((stats.mediumPriority / total) * 100).toFixed(1)
                    : 0,
            color: "#f97316",
        },
        {
            label: "Low",
            value: stats.lowPriority,
            percentage:
                total > 0 ? ((stats.lowPriority / total) * 100).toFixed(1) : 0,
            color: "#22c55e",
        },
    ];

    const maxValue = Math.max(
        stats.highPriority,
        stats.mediumPriority,
        stats.lowPriority
    );

    return (
        <div className="priority-chart">
            <div className="chart-bars">
                {chartData.map((item, index) => (
                    <div key={index} className="chart-bar-container">
                        <div className="chart-label">{item.label}</div>
                        <div className="chart-bar-wrapper">
                            <div
                                className="chart-bar"
                                style={{
                                    width: `${
                                        maxValue > 0
                                            ? (item.value / maxValue) * 100
                                            : 0
                                    }%`,
                                    backgroundColor: item.color,
                                }}
                            >
                                <span className="chart-value">
                                    {item.value}
                                </span>
                            </div>
                        </div>
                        <div className="chart-percentage">
                            {item.percentage}%
                        </div>
                    </div>
                ))}
            </div>

            <div className="chart-summary">
                <div className="summary-item">
                    <span className="summary-label">Total Vehicles:</span>
                    <span className="summary-value">{total}</span>
                </div>
                <div className="summary-item">
                    <span className="summary-label">Plates Detected:</span>
                    <span className="summary-value">
                        {stats.withPlates} / {stats.totalDetections}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default PriorityChart;
