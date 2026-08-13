function SensorCard({ event }) {
  if (!event) {
    return null;
  }

  const isAnomaly = event.prediction === "ANOMALY";

  return (
    <div className={`sensor-card ${isAnomaly ? "sensor-anomaly" : ""}`}>
      <div className="sensor-card-header">
        <div>
          <h3>Sensor</h3>
          <p>{event.device_id?.slice(0, 8)}...</p>
        </div>

        <span
          className={`badge ${
            isAnomaly ? "anomaly" : "normal"
          }`}
        >
          {event.prediction}
        </span>
      </div>

      <div className="sensor-values">
        <div>
          <span>Temperature</span>
          <strong>{event.temperature}°</strong>
        </div>

        <div>
          <span>Pressure</span>
          <strong>{event.pressure}</strong>
        </div>

        <div>
          <span>Vibration</span>
          <strong>{event.vibration}</strong>
        </div>
      </div>
    </div>
  );
}

export default SensorCard;