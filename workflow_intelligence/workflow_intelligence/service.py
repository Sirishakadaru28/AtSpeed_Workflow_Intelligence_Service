
import json
from datetime import datetime

from sqlalchemy.orm import Session

from .models import WorkItem
from .schemas import WorkItemCreate
from .ml.predictor import predict_risk


def calculate_hours_until_due(due_date: datetime) -> float:
    now = datetime.utcnow()

    hours = (due_date - now).total_seconds() / 3600

    return max(hours, 0)


def create_work_item(
    db: Session,
    work_item_data: WorkItemCreate
):
    hours_until_due = calculate_hours_until_due(
        work_item_data.due_date
    )

    prediction = predict_risk(
        category=work_item_data.category,
        priority=work_item_data.priority.value,
        status=work_item_data.status.value,
        estimated_hours=work_item_data.estimated_hours,
        dependency_count=work_item_data.dependency_count,
        issue_count=work_item_data.issue_count,
        hours_since_update=work_item_data.hours_since_update,
        hours_until_due=hours_until_due
    )

    work_item = WorkItem(
        title=work_item_data.title,
        description=work_item_data.description,
        category=work_item_data.category,
        priority=work_item_data.priority.value,
        status=work_item_data.status.value,
        estimated_hours=work_item_data.estimated_hours,
        dependency_count=work_item_data.dependency_count,
        issue_count=work_item_data.issue_count,
        hours_since_update=work_item_data.hours_since_update,
        due_date=work_item_data.due_date,
        risk_level=prediction["risk_level"],
        risk_score=prediction["risk_score"],
        top_factors=json.dumps(
            prediction["top_factors"]
        )
    )

    db.add(work_item)
    db.commit()
    db.refresh(work_item)

    return work_item


def get_work_item(db: Session, work_item_id: int):
    return (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )


def get_work_items(
    db: Session,
    status=None,
    risk_level=None
):
    query = db.query(WorkItem)

    if status:
        query = query.filter(
            WorkItem.status == status
        )

    if risk_level:
        query = query.filter(
            WorkItem.risk_level == risk_level
        )

    return query.order_by(
        WorkItem.created_at.desc()
    ).all()


def get_prioritized_work_items(db: Session):

    return (
        db.query(WorkItem)
        .order_by(
            WorkItem.risk_score.desc()
        )
        .all()
    )
