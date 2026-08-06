export default function EventTable({ events }) {

    return (

        <table className="table-auto w-full border mt-8">

            <thead>

                <tr>

                    <th>ID</th>

                    <th>Temperature</th>

                    <th>Pressure</th>

                    <th>Status</th>

                </tr>

            </thead>

            <tbody>

                {events.map((event) => (

                    <tr key={event.id}>

                        <td>{event.id}</td>

                        <td>{event.temperature.toFixed(2)}</td>

                        <td>{event.pressure.toFixed(2)}</td>

                        <td>

                            <span
                                className={
                                    event.status === "ANOMALY"
                                        ? "bg-red-100"
                                        : ""

                                }
                            >
                                {event.status}
                            </span>

                        </td>

                    </tr>

                ))}

            </tbody>

        </table>

    );

}