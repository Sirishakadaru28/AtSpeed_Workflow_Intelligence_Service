
# AtSpeed Workflow Intelligence Service

## 1. Project Overview

AtSpeed Workflow Intelligence Service is a backend service that analyzes work items and predicts their operational risk.

The system combines:

- FastAPI for REST APIs
- SQLite for persistent data storage
- SQLAlchemy for database interaction
- A Random Forest machine learning model for risk prediction
- Pytest for automated API testing

For each work item, the system analyzes attributes such as priority, status, estimated effort, dependencies, issues, update history, and time remaining until the due date.

The system predicts one of three risk levels:

- LOW
- MEDIUM
- HIGH

The prediction also includes a numerical risk score and the main factors contributing to the predicted risk.

---

## 2. Key Features

### Work Item Management

The service supports:

- Creating work items
- Retrieving a work item by ID
- Retrieving all work items
- Filtering work items by status
- Filtering work items by risk level

### Machine Learning Risk Prediction

The machine learning pipeline predicts:

- Risk level
- Risk score
- Top contributing risk factors

### Prioritized Work Queue

Work items can be retrieved in descending order of risk score.

This allows high-risk work items to be identified and addressed first.

### Database Persistence

Work items are stored in a SQLite database using SQLAlchemy.

### Automated Testing

The project includes automated API tests covering:

1. Health check
2. Risk prediction
3. Work-item creation
4. Work-item retrieval
5. Nonexistent work-item handling
6. Prioritized work items

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| API Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Machine Learning | scikit-learn |
| ML Algorithm | Random Forest Classifier |
| Model Serialization | Joblib |
| Data Processing | Pandas |
| Testing | Pytest |
| API Testing | FastAPI TestClient / HTTPX |

---

## 4. Project Structure

```text
workflow_intelligence/
│
├── README.md
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── service.py
│
├── api/
│   ├── __init__.py
│   └── routes.py
│
├── ml/
│   ├── __init__.py
│   └── predictor.py
│
├── models/
│   └── risk_model.joblib
│
├── data/
│   └── training_data.csv
│
└── tests/
    └── test_api.py

---

## Main Features

- Machine learning based work-item risk prediction
- Risk levels: LOW, MEDIUM, HIGH
- Risk score generation
- Identification of top risk factors
- Work-item creation and storage
- Work-item retrieval
- Status and risk-level filtering
- Risk-based prioritized queue
- 404 handling for nonexistent work items
- Automated API testing

---

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Scikit-learn
- Joblib
- Pytest
- Uvicorn

---

## API Endpoints

### Health Check

```text
GET /api/v1/health
