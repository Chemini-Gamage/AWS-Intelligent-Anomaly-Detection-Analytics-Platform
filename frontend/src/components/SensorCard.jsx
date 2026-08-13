function SensorCard({ event }) {
  if (!event) {
    return (
      <div className="sensor-card">
        <div className="sensor-card-header">
          <div>
            <h3>Latest Sensor Reading</h3>
            <p>No sensor data available</p>
          </div>
        </div>

        <div className="empty-state">
          Waiting for sensor data...
        </div>
      </div>
    );
  }

  const isAnomaly = event.prediction === "ANOMALY";

  return (
    <div
      className={`sensor-card ${
        isAnomaly ? "sensor-anomaly" : ""
      }`}
    >
      <div className="sensor-card-header">
        <div>
          <h3>Latest Sensor Reading</h3>

          <p>
            Device:{" "}
            {event.device_id
              ? `${event.device_id.slice(0, 8)}...`
              : "Unknown"}
          </p>
        </div>

        <span
          className={
            isAnomaly
              ? "badge anomaly"
              : "badge normal"
          }
        >
          {event.prediction || "UNKNOWN"}
        </span>
      </div>

      <div className="sensor-values">
        <div>
          <span>Temperature</span>
          <strong>
            {event.temperature ?? "-"}°
          </strong>
        </div>

        <div>
          <span>Pressure</span>
          <strong>
            {event.pressure ?? "-"}
          </strong>
        </div>

        <div>
          <span>Vibration</span>
          <strong>
            {event.vibration ?? "-"}
          </strong>
        </div>
      </div>

      <div className="sensor-timestamp">
        Last reading:{" "}
        {event.timestamp
          ? new Date(event.timestamp).toLocaleString()
          : "-"}
      </div>
    </div>
  );
}

export default SensorCard;