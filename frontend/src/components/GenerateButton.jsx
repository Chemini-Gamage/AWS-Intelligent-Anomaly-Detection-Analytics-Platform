import api from "../services/api";

export default function GenerateButton({ refresh }) {

    async function generateEvent() {

        await api.post("/events");

        refresh();

    }

    return (

        <button
            onClick={generateEvent}
            className="bg-blue-600 text-white px-5 py-3 rounded-lg hover:bg-blue-700 transition"
        >
            Generate Sensor Event
        </button>

    );

}