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


## 3. Project Structure

```text
ATSpeed_Workflow_Intelligence_Service/
├── README.md
├── main.py
├── database.py
├── models.py
├── schemas.py
├── service.py
├── api/
├── ml/
├── models/
├── data/
├── tests/
├── architecture.png
└── database_er_diagram.png

---

## 6. Data Model

Each work item contains information such as:

- ID
- Title
- Description
- Category
- Priority
- Status
- Estimated hours
- Dependency count
- Issue count
- Hours since update
- Due date
- Risk level
- Risk score
- Top risk factors
- Created timestamp

Supported priority levels:

LOW
MEDIUM
HIGH

Supported status values:

OPEN
IN_PROGRESS
BLOCKED
DONE

---

## 7. Machine Learning Approach

The project uses a Random Forest Classifier to predict work-item risk.

### Input Features

The model uses:

- Category
- Priority
- Status
- Estimated hours
- Dependency count
- Issue count
- Hours since update
- Hours until due date

### Output

The model produces:

- Risk level
- Risk probability/score
- Interpretable risk factors

The trained model is stored using Joblib at:

models/risk_model.joblib

The prediction logic is implemented in:

ml/predictor.py

---

## 8. Database

The application uses SQLite for lightweight persistent storage.

The database interaction is handled using SQLAlchemy.

Main database file:

database.py

The database stores work items and their calculated risk information.

---

## 9. Architecture

The overall request flow is:

Client
   |
   v
FastAPI
   |
   v
API Routes
   |
   v
Service Layer
   |
   +----------------+
   |                |
   v                v
ML Predictor     SQLAlchemy
   |                |
   v                v
Random Forest     SQLite

The detailed architecture diagram is available at:

architecture.png

The database ER diagram is available at:

database_er_diagram.png

---

## 10. Installation

Clone the repository and navigate to the project directory.

Install the required dependencies:

pip install fastapi uvicorn sqlalchemy pydantic scikit-learn joblib pandas pytest httpx

---

## 11. Running the Application

Start the FastAPI server using:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

FastAPI interactive documentation:

http://127.0.0.1:8000/docs

---

## 12. Running Tests

Run the automated tests using:

pytest tests/test_api.py -v

The tests verify the main API functionality and risk prediction workflow.

---

## 13. Example Work Item

Example request:

{
  "title": "Resolve payment gateway issue",
  "description": "Investigate and resolve payment processing failure",
  "category": "Support",
  "priority": "HIGH",
  "status": "BLOCKED",
  "estimated_hours": 20,
  "dependency_count": 3,
  "issue_count": 5,
  "hours_since_update": 50,
  "due_date": "2026-08-30T18:00:00"
}

The service calculates the risk automatically and returns the work item together with its risk information.

---

## 14. Risk-Based Prioritization

The prioritized endpoint:

GET /api/v1/work-items/prioritized

returns work items ordered by descending risk score.

This helps identify the work items that require attention first.

---

## 15. Testing Coverage

The automated tests verify:

- API health
- Risk prediction
- Work-item creation
- Work-item retrieval
- Work-item listing
- Invalid/nonexistent work-item handling
- Risk-based prioritization

---

## 16. Known Limitations

- The current model is trained on a limited dataset.
- Risk predictions depend on the quality of the training data.
- SQLite is suitable for this assignment but may not be ideal for large-scale production workloads.
- Authentication and authorization are outside the scope of this project.
- Production deployment and distributed infrastructure are outside the scope of this implementation.

---

## 17. Future Improvements

Possible future improvements include:

- Larger and continuously updated training datasets
- Model retraining pipelines
- More advanced explainability techniques
- PostgreSQL for production-scale storage
- Authentication and authorization
- Monitoring and logging
- Model performance monitoring
- Automated CI/CD
- Production deployment

---

## 18. Project Objective

The objective of this project is to provide a practical workflow intelligence service that combines backend engineering, database persistence, and machine learning.

The final system allows users to:

1. Create work items
2. Automatically calculate risk
3. Store work items in a database
4. Retrieve and filter work items
5. Identify high-risk work items
6. View a prioritized queue
7. Test the API automatically
