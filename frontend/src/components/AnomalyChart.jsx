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
    const normal = statistics?.normal_events ?? 0;
    const anomalies = statistics?.anomalies ?? 0;

    const data = {
        labels: ["Normal", "Anomalies"],
        datasets: [
            {
                data: [normal, anomalies],
                borderWidth: 0,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                position: "bottom",
            },
        },

        cutout: "70%",
    };

    return (
        <div className="chart-card">
            <div className="chart-header">
                <div>
                    <h2>Event Distribution</h2>
                    <p>Normal vs anomalous sensor events</p>
                </div>
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