function StatCard({ title, value, type = "" }) {
    return (
        <div className={`stat-card ${type}`}>
            <span>{title}</span>
            <strong>{value}</strong>
        </div>
    );
}

export default StatCard;