export default function StatsCards({ stats }) {

    return (

        <div className="grid grid-cols-3 gap-6 mb-8">

            <div className="bg-blue-100 p-6 rounded">

                <h2>Total Events</h2>

                <h1 className="text-4xl">

                    {stats.total_events || 0}

                </h1>

            </div>

            <div className="bg-green-100 p-6 rounded">

                <h2>Normal</h2>

                <h1 className="text-4xl">

                    {stats.normal_events || 0}

                </h1>

            </div>

            <div className="bg-red-100 p-6 rounded">

                <h2>Anomalies</h2>

                <h1 className="text-4xl">

                    {stats.anomalies || 0}

                </h1>

            </div>
            <div className="bg-yellow-100 p-6 rounded">

                <h2>Anomaly Rate</h2>

                <h1 className="text-4xl">

                    {
                        stats.total_events
                            ? (
                                stats.anomalies /
                                stats.total_events *
                                100
                            ).toFixed(1)
                            : 0
                    }%

                </h1>

            </div>
        </div>

    );

}