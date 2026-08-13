import { useEffect, useState } from "react";
import { getStatistics, getEvents, checkHealth } from "./services/api";
import "./App.css";

function App() {
  const [statistics, setStatistics] = useState(null);
  const [events, setEvents] = useState([]);
  const [apiStatus, setApiStatus] = useState("Checking...");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setError("");

      const [statsData, eventsData] = await Promise.all([
        getStatistics(),
        getEvents(),
      ]);

      setStatistics(statsData);

      setEvents(
        Array.isArray(eventsData)
          ? eventsData
          : eventsData.events || []
      );

      try {
        await checkHealth();
        setApiStatus("Operational");
      } catch {
        setApiStatus("Unavailable");
      }
    } catch (err) {
      console.error(err);
      setError("Unable to load dashboard data.");
      setApiStatus("Unavailable");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(loadDashboard, 10000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <h1>Industrial Sensor Intelligence</h1>
        <p>Connecting to AWS...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Industrial Sensor Intelligence</h1>
          <p>AWS Real-Time Anomaly Monitoring Platform</p>
        </div>

        <div className="status">
          <span
            className={
              apiStatus === "Operational"
                ? "status-dot online"
                : "status-dot offline"
            }
          />

          API {apiStatus}
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      <main>
        <section className="stats-grid">
          <div className="stat-card">
            <span>Total Events</span>
            <strong>{statistics?.total_events ?? 0}</strong>
          </div>

          <div className="stat-card">
            <span>Normal Events</span>
            <strong>{statistics?.normal_events ?? 0}</strong>
          </div>

          <div className="stat-card anomaly-card">
            <span>Anomalies</span>
            <strong>{statistics?.anomalies ?? 0}</strong>
          </div>

          <div className="stat-card">
            <span>Anomaly Rate</span>
            <strong>
              {statistics?.anomaly_rate ?? 0}%
            </strong>
          </div>
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <h2>Recent Sensor Events</h2>
              <p>Latest events processed by the AWS pipeline</p>
            </div>

            <button onClick={loadDashboard}>
              Refresh
            </button>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Device</th>
                  <th>Temperature</th>
                  <th>Pressure</th>
                  <th>Vibration</th>
                  <th>Prediction</th>
                  <th>Timestamp</th>
                </tr>
              </thead>

              <tbody>
                {events.slice(0, 20).map((event) => (
                  <tr key={event.id}>
                    <td>{event.device_id?.slice(0, 8)}...</td>
                    <td>{event.temperature}°</td>
                    <td>{event.pressure}</td>
                    <td>{event.vibration}</td>

                    <td>
                      <span
                        className={
                          event.prediction === "ANOMALY"
                            ? "badge anomaly"
                            : "badge normal"
                        }
                      >
                        {event.prediction}
                      </span>
                    </td>

                    <td>
                      {event.timestamp
                        ? new Date(event.timestamp).toLocaleString()
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;