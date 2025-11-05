import React from "react";
import { Video, WifiOff } from "lucide-react";

const LiveFeed = ({ isConnected }) => {
    return (
        <div className="card live-feed-card">
            <div className="card-header">
                <h3>Live Camera Feed</h3>
                <Video size={20} className="card-icon" />
            </div>
            <div className="live-feed-content">
                {isConnected ? (
                    <div className="video-placeholder">
                        <div className="video-frame">
                            <div className="video-overlay">
                                <div className="detection-box box-green">
                                    <span className="detection-label">
                                        car [LOW] | ABC1234
                                    </span>
                                </div>
                                <div className="detection-box box-orange">
                                    <span className="detection-label">
                                        truck [MEDIUM] | XYZ9876
                                    </span>
                                </div>
                            </div>
                            <div className="video-info">
                                <span>🟢 Live</span>
                                <span>1920x1080</span>
                                <span>30 FPS</span>
                            </div>
                        </div>
                        <p className="feed-note">
                            Connect to ESP32-CAM or video source to view live
                            feed
                        </p>
                    </div>
                ) : (
                    <div className="disconnected-state">
                        <WifiOff size={48} />
                        <p>Camera disconnected</p>
                        <button className="btn btn-primary">
                            Connect Camera
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LiveFeed;
