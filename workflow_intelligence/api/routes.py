
import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import (
    WorkItemCreate,
    WorkItemResponse,
    RiskPrediction,
    Status,
    RiskLevel
)

from ..service import (
    create_work_item as create_work_item_service,
    get_work_item,
    get_work_items,
    get_prioritized_work_items
)

from ..ml.predictor import predict_risk


router = APIRouter()


def format_work_item(work_item):
    """Convert database object into API response format."""

    if isinstance(work_item.top_factors, str):
        top_factors = json.loads(work_item.top_factors)
    else:
        top_factors = work_item.top_factors

    return {
        "id": work_item.id,
        "title": work_item.title,
        "description": work_item.description,
        "category": work_item.category,
        "priority": work_item.priority,
        "status": work_item.status,
        "estimated_hours": work_item.estimated_hours,
        "dependency_count": work_item.dependency_count,
        "issue_count": work_item.issue_count,
        "hours_since_update": work_item.hours_since_update,
        "due_date": work_item.due_date,
        "risk_level": work_item.risk_level,
        "risk_score": work_item.risk_score,
        "top_factors": top_factors,
        "created_at": work_item.created_at
    }


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# -------------------------------------------------
# Create Work Item
# -------------------------------------------------

@router.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=201
)
def create_work_item_endpoint(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):

    created_item = create_work_item_service(
        db,
        work_item
    )

    return format_work_item(created_item)


# -------------------------------------------------
# List Work Items
# -------------------------------------------------

@router.get(
    "/work-items",
    response_model=list[WorkItemResponse]
)
def list_work_items(
    status: Status | None = Query(default=None),
    risk_level: RiskLevel | None = Query(default=None),
    db: Session = Depends(get_db)
):

    items = get_work_items(
        db=db,
        status=status.value if status else None,
        risk_level=risk_level.value if risk_level else None
    )

    return [
        format_work_item(item)
        for item in items
    ]


# -------------------------------------------------
# Prioritized Queue
# -------------------------------------------------

@router.get(
    "/work-items/prioritized",
    response_model=list[WorkItemResponse]
)
def prioritized_work_items(
    db: Session = Depends(get_db)
):

    items = get_prioritized_work_items(db)

    return [
        format_work_item(item)
        for item in items
    ]


# -------------------------------------------------
# Get Single Work Item
# -------------------------------------------------

@router.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_single_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):

    work_item = get_work_item(
        db,
        work_item_id
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return format_work_item(work_item)


# -------------------------------------------------
# Predict Risk
# -------------------------------------------------

@router.post(
    "/risk/predict",
    response_model=RiskPrediction
)
def predict_work_item_risk(
    work_item: WorkItemCreate
):

    now = datetime.utcnow()

    hours_until_due = (
        work_item.due_date - now
    ).total_seconds() / 3600

    hours_until_due = max(
        hours_until_due,
        0
    )

    prediction = predict_risk(
        category=work_item.category,
        priority=work_item.priority.value,
        status=work_item.status.value,
        estimated_hours=work_item.estimated_hours,
        dependency_count=work_item.dependency_count,
        issue_count=work_item.issue_count,
        hours_since_update=work_item.hours_since_update,
        hours_until_due=hours_until_due
    )

    return prediction
