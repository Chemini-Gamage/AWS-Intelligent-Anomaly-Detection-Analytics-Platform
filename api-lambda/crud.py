from sqlalchemy.orm import Session

import models

from dynamodb_service import get_all_events as get_dynamodb_events


def create_event(db: Session, event):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_events(db: Session):
    return db.query(models.Event).all()


def get_statistics():

    events = get_dynamodb_events()

    print(f"DEBUG: DynamoDB events retrieved: {len(events)}")

    if events:
        print(f"DEBUG: First event: {events[0]}")
        print(f"DEBUG: First prediction: {events[0].get('prediction')}")

    anomalies = sum(
        1
        for event in events
        if event.get("prediction") == "ANOMALY"
    )

    total = len(events)
    normal = total - anomalies

    anomaly_rate = (
        (anomalies / total) * 100
        if total > 0
        else 0
    )

    print(f"DEBUG: Total: {total}")
    print(f"DEBUG: Normal: {normal}")
    print(f"DEBUG: Anomalies: {anomalies}")

    return {
        "total_events": total,
        "normal_events": normal,
        "anomalies": anomalies,
        "anomaly_rate": round(anomaly_rate, 2)
    }