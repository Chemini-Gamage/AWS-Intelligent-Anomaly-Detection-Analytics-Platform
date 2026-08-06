import {

    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid

} from "recharts";

export default function Charts({ events }) {

    return (

        <LineChart
            width={900}
            height={350}
            data={events}
        >

            <CartesianGrid />

            <XAxis dataKey="id" />

            <YAxis />

            <Tooltip />

            <Line
                type="monotone"
                dataKey="temperature"
                stroke="#2563eb"
            />

            <Line
                type="monotone"
                dataKey="pressure"
                stroke="#16a34a"
            />

        </LineChart>

    );

}