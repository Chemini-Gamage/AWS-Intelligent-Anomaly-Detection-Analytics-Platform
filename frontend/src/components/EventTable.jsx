function EventTable({ events }) {
    return (
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
                    {events.length === 0 ? (
                        <tr>
                            <td colSpan="6" className="empty-state">
                                No sensor events available.
                            </td>
                        </tr>
                    ) : (
                        events.slice(0, 20).map((event) => (
                            <tr key={event.id}>
                                <td>
                                    {event.device_id
                                        ? `${event.device_id.slice(0, 8)}...`
                                        : "-"}
                                </td>

                                <td>
                                    {event.temperature ?? "-"}°
                                </td>

                                <td>
                                    {event.pressure ?? "-"}
                                </td>

                                <td>
                                    {event.vibration ?? "-"}
                                </td>

                                <td>
                                    <span
                                        className={
                                            event.prediction === "ANOMALY"
                                                ? "badge anomaly"
                                                : "badge normal"
                                        }
                                    >
                                        {event.prediction || "UNKNOWN"}
                                    </span>
                                </td>

                                <td>
                                    {event.timestamp
                                        ? new Date(event.timestamp).toLocaleString()
                                        : "-"}
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}

export default EventTable;