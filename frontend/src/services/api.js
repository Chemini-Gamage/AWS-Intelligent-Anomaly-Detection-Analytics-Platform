const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getStatistics() {
    const response = await fetch(`${API_BASE_URL}/statistics`);

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
}

export async function getEvents() {
    const response = await fetch(`${API_BASE_URL}/events`);

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
}

export async function checkHealth() {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
}