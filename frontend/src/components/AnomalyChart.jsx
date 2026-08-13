import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
} from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend
);

function AnomalyChart({ statistics }) {
    const normal = Number(statistics?.normal_events ?? 0);
    const anomalies = Number(statistics?.anomalies ?? 0);

    const data = {
        labels: ["Normal Events", "Anomalies"],
        datasets: [
            {
                data: [normal, anomalies],
                backgroundColor: [
                    "#22c55e",
                    "#ef4444",
                ],
                borderColor: [
                    "#16a34a",
                    "#dc2626",
                ],
                borderWidth: 2,
                hoverOffset: 8,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "65%",
        plugins: {
            legend: {
                position: "bottom",
                labels: {
                    padding: 20,
                    usePointStyle: true,
                },
            },
        },
    };

    return (
        <div className="chart-card">
            <div className="chart-header">
                <h2>Event Distribution</h2>
                <p>Normal vs anomaly events</p>
            </div>

            <div className="chart-container">
                <Doughnut
                    data={data}
                    options={options}
                />
            </div>
        </div>
    );
}

export default AnomalyChart;