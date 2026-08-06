import { useEffect, useState } from "react";
import api from "../services/api";

import StatsCards from "./StatsCards";
import EventTable from "./EventTable";
import Charts from "./Charts";
//generate button
import GenerateButton from "./GenerateButton";

export default function Dashboard() {

    const [events, setEvents] = useState([]);
    const [stats, setStats] = useState({});

    const loadData = async () => {

        const eventsRes = await api.get("/events");
        const statsRes = await api.get("/statistics");

        setEvents(eventsRes.data);
        setStats(statsRes.data);

    };

    useEffect(() => {

        loadData();

        const timer = setInterval(loadData, 5000);

        return () => clearInterval(timer);

    }, []);

    return (

        <div className="p-10">

            <h1 className="text-4xl font-bold mb-8">

                AWS Analytics Dashboard

            </h1>
            <GenerateButton refresh={loadData} />

            <div className="mt-8">
                <StatsCards stats={stats} />
            </div>

            <StatsCards stats={stats} />

            <Charts events={events} />

            <EventTable events={events} />


        </div>

    );

}