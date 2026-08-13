import { useEffect, useState } from "react";

import {
  getStatistics,
  getEvents,
  checkHealth,
} from "./services/api";

import Header from "./components/Header";
import StatCard from "./components/StatCard";
import SensorCard from "./components/SensorCard";
import EventTable from "./components/EventTable";
import AnomalyChart from "./components/AnomalyChart";
import AnomalyAnalysis from "./components/AnomalyAnalysis";
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

      const receivedEvents = Array.isArray(eventsData)
        ? eventsData
        : eventsData.events || [];

      const sortedEvents = [...receivedEvents].sort(
        (a, b) =>
          new Date(b.timestamp) - new Date(a.timestamp)
      );

      setEvents(sortedEvents);
      try {
        await checkHealth();
        setApiStatus("Operational");
      } catch {
        setApiStatus("Unavailable");
      }
    } catch (err) {
      console.error(err);

      setError(
        "Unable to load dashboard data."
      );

      setApiStatus("Unavailable");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(
      loadDashboard,
      10000
    );

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <h1>
          Industrial Sensor Intelligence
        </h1>

        <p>
          Connecting to AWS...
        </p>
      </div>
    );
  }

  return (
    <div className="app">

      <Header apiStatus={apiStatus} />

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <main>

        {/* STATISTICS */}

        <section className="stats-grid">

          <StatCard
            title="Total Events"
            value={
              statistics?.total_events ?? 0
            }
          />

          <StatCard
            title="Normal Events"
            value={
              statistics?.normal_events ?? 0
            }
          />

          <StatCard
            title="Anomalies"
            value={
              statistics?.anomalies ?? 0
            }
            type="anomaly-card"
          />

          <StatCard
            title="Anomaly Rate"
            value={`${statistics?.anomaly_rate ?? 0
              }%`}
          />

        </section>


        {/* CHART + SENSOR */}

        <section className="dashboard-grid">

          <AnomalyChart
            statistics={statistics}
          />

          {events.length > 0 && (
            <SensorCard
              event={events[0]}
            />
          )}
          <AnomalyAnalysis events={events} />

        </section>


        {/* EVENTS */}

        <section className="panel">

          <div className="panel-header">

            <div>
              <h2>
                Recent Sensor Events
              </h2>

              <p>
                Latest events processed by
                the AWS pipeline
              </p>
            </div>

            <button
              onClick={loadDashboard}
            >
              Refresh
            </button>

          </div>

          <EventTable
            events={events}
          />

        </section>

      </main>

    </div>
  );
}

export default App;