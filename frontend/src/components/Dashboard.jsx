import { useEffect, useState } from "react";
import {
    getStatistics,
    getEvents,
    checkHealth,
} from "../services/api";

import StatsCards from "./StatsCards";
import EventTable from "./EventTable";
import Charts from "./Charts";
import GenerateButton from "./GenerateButton";

export default function Dashboard() {
    const [events, setEvents] = useState([]);
    const [stats, setStats] = useState({});
    const [health, setHealth] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadData = async () => {
        try {
            setError(null);

            const [healthData, statsData, eventsData] = await Promise.all([
                checkHealth(),
                getStatistics(),
                getEvents(),
            ]);

            setHealth(healthData);
            setStats(statsData);
            setEvents(eventsData);
        } catch (err) {
            console.error("Failed to load dashboard data:", err);
            setError(err.message || "Failed to load dashboard data");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();

        const timer = setInterval(loadData, 5000);

        return () => clearInterval(timer);
    }, []);

    return (
        <div className="p-10">

            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-4xl font-bold">
                        AWS Analytics Dashboard
                    </h1>

                    <div className="mt-2">
                        API Status:{" "}
                        {health?.status === "healthy" ? (
                            <span className="text-green-600 font-semibold">
                                Operational
                            </span>
                        ) : (
                            <span className="text-red-600 font-semibold">
                                Unavailable
                            </span>
                        )}
                    </div>
                </div>

                <button
                    onClick={loadData}
                    disabled={loading}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                    {loading ? "Refreshing..." : "Refresh"}
                </button>
            </div>

            {error && (
                <div className="mb-6 p-4 bg-red-100 text-red-700 rounded-lg">
                    Failed to load dashboard data: {error}
                </div>
            )}

            <GenerateButton refresh={loadData} />

            <div className="mt-8">
                <StatsCards stats={stats} />
            </div>

            <Charts events={events} />

            <EventTable events={events} />

        </div>
    );
}