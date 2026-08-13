function Header({ apiStatus }) {
    return (
        <header className="header">
            <div>
                <h1>Industrial Sensor Intelligence</h1>
                <p>AWS Real-Time Anomaly Monitoring Platform</p>
            </div>

            <div className="status">
                <span
                    className={
                        apiStatus === "Operational"
                            ? "status-dot online"
                            : "status-dot offline"
                    }
                />

                API {apiStatus}
            </div>
        </header>
    );
}

export default Header;