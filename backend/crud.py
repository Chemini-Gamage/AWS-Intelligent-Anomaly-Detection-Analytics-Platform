from sqlalchemy.orm import Session

import models



def create_event(db, event):

    db.add(event)

    db.commit()

    db.refresh(event)

    return event


def get_events(db):

    return db.query(models.Event).all()


def get_statistics(db):

    total = db.query(models.Event).count()

    anomalies = db.query(models.Event).filter(
        models.Event.status == "ANOMALY"
    ).count()

    return {

        "total_events": total,

        "normal_events": total - anomalies,

        "anomalies": anomalies

    }