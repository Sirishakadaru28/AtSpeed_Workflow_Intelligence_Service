
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Status(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    DONE = "DONE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class WorkItemCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    description: str = Field(
        ...,
        min_length=1
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    priority: Priority

    status: Status

    estimated_hours: float = Field(
        ...,
        gt=0
    )

    dependency_count: int = Field(
        ...,
        ge=0
    )

    issue_count: int = Field(
        ...,
        ge=0
    )

    hours_since_update: float = Field(
        ...,
        ge=0
    )

    due_date: datetime


class RiskPrediction(BaseModel):

    risk_level: RiskLevel

    risk_score: float = Field(
        ...,
        ge=0,
        le=1
    )

    top_factors: List[str]


class WorkItemResponse(BaseModel):

    id: int
    title: str
    description: str
    category: str
    priority: Priority
    status: Status
    estimated_hours: float
    dependency_count: int
    issue_count: int
    hours_since_update: float
    due_date: datetime
    risk_level: RiskLevel
    risk_score: float
    top_factors: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
