function AnomalyAnalysis({ events }) {
    const anomalies = events
        .filter((event) => event.prediction === "ANOMALY")
        .sort(
            (a, b) =>
                new Date(b.timestamp) -
                new Date(a.timestamp)
        );

    const latestAnomaly = anomalies[0];

    if (!latestAnomaly) {
        return (
            <section className="panel anomaly-analysis">
                <div className="panel-header">
                    <div>
                        <h2>Anomaly Analysis</h2>
                        <p>Recent abnormal sensor activity</p>
                    </div>
                </div>

                <div className="empty-state">
                    <h3>No anomalies detected</h3>
                    <p>
                        All recent sensor readings are within
                        normal operating conditions.
                    </p>
                </div>
            </section>
        );
    }

    return (
        <section className="panel anomaly-analysis">
            <div className="panel-header">
                <div>
                    <h2>Anomaly Analysis</h2>
                    <p>Latest abnormal sensor activity</p>
                </div>

                <span className="badge anomaly">
                    ANOMALY DETECTED
                </span>
            </div>

            <div className="anomaly-analysis-content">
                <div className="anomaly-device">
                    <span>Device</span>

                    <strong>
                        {latestAnomaly.device_id
                            ? `${latestAnomaly.device_id.slice(0, 8)}...`
                            : "Unknown"}
                    </strong>
                </div>

                <div className="anomaly-values">

                    <div>
                        <span>Temperature</span>
                        <strong>
                            {latestAnomaly.temperature ?? "-"}°
                        </strong>
                    </div>

                    <div>
                        <span>Pressure</span>
                        <strong>
                            {latestAnomaly.pressure ?? "-"}
                        </strong>
                    </div>

                    <div>
                        <span>Vibration</span>
                        <strong>
                            {latestAnomaly.vibration ?? "-"}
                        </strong>
                    </div>

                </div>

                <div className="anomaly-details">

                    <div>
                        <span>Prediction</span>

                        <strong className="anomaly-text">
                            {latestAnomaly.prediction}
                        </strong>
                    </div>

                    <div>
                        <span>Detected</span>

                        <strong>
                            {latestAnomaly.timestamp
                                ? new Date(
                                    latestAnomaly.timestamp
                                ).toLocaleString()
                                : "-"}
                        </strong>
                    </div>

                </div>
            </div>
        </section>
    );
}

export default AnomalyAnalysis;