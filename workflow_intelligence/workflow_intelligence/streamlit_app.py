
import streamlit as st
import requests
from datetime import datetime, timedelta


st.set_page_config(
    page_title="AtSpeed Workflow Intelligence",
    page_icon="⚠️",
    layout="wide"
)


# -------------------------------------------------
# Configuration
# -------------------------------------------------

st.title("⚠️ AtSpeed Workflow Intelligence")
st.caption("ML-powered Work Item Risk Prediction & Prioritization")


# Enter your running FastAPI service URL
API_URL = st.sidebar.text_input(
    "FastAPI Service URL",
    value="http://127.0.0.1:8003"
).rstrip("/")


st.sidebar.markdown("---")
st.sidebar.info(
    "This Streamlit application communicates "
    "with the FastAPI backend through HTTP APIs."
)


# -------------------------------------------------
# Helper
# -------------------------------------------------

def make_payload():

    return {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": status,
        "estimated_hours": estimated_hours,
        "dependency_count": dependency_count,
        "issue_count": issue_count,
        "hours_since_update": hours_since_update,
        "due_date": due_date.isoformat()
    }


# -------------------------------------------------
# Input Section
# -------------------------------------------------

st.header("Work Item")

col1, col2 = st.columns(2)

with col1:

    title = st.text_input(
        "Title",
        value="Production Database Issue"
    )

    description = st.text_area(
        "Description",
        value="Critical database issue affecting production"
    )

    category = st.selectbox(
        "Category",
        ["Support", "Development", "Bug", "Maintenance"]
    )

    priority = st.selectbox(
        "Priority",
        ["LOW", "MEDIUM", "HIGH"]
    )


with col2:

    status = st.selectbox(
        "Status",
        ["OPEN", "IN_PROGRESS", "BLOCKED", "COMPLETED"]
    )

    estimated_hours = st.number_input(
        "Estimated Hours",
        min_value=0,
        value=30
    )

    dependency_count = st.number_input(
        "Dependency Count",
        min_value=0,
        value=5
    )

    issue_count = st.number_input(
        "Issue Count",
        min_value=0,
        value=8
    )

    hours_since_update = st.number_input(
        "Hours Since Update",
        min_value=0,
        value=100
    )

    due_date = st.date_input(
        "Due Date",
        value=datetime.utcnow().date() + timedelta(days=1)
    )


# -------------------------------------------------
# API Buttons
# -------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)


# -------------------------------------------------
# Risk Prediction
# -------------------------------------------------

with col1:

    if st.button(
        "🔮 Predict Risk",
        use_container_width=True
    ):

        payload = make_payload()

        try:

            response = requests.post(
                f"{API_URL}/api/v1/risk/predict",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:

                data = response.json()

                st.success("Risk prediction successful!")

                risk = data.get("risk_level", "UNKNOWN")
                score = data.get("risk_score", 0)

                st.metric(
                    "Risk Level",
                    risk
                )

                st.metric(
                    "Risk Score",
                    f"{score:.3f}"
                )

                st.subheader("Top Risk Factors")

                for factor in data.get(
                    "top_factors",
                    []
                ):
                    st.write(f"• {factor}")

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.json(response.json())

        except Exception as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )


# -------------------------------------------------
# Create Work Item
# -------------------------------------------------

with col2:

    if st.button(
        "➕ Create Work Item",
        use_container_width=True
    ):

        payload = make_payload()

        try:

            response = requests.post(
                f"{API_URL}/api/v1/work-items",
                json=payload,
                timeout=30
            )

            if response.status_code == 201:

                data = response.json()

                st.success(
                    f"Work item created successfully! "
                    f"ID: {data.get('id')}"
                )

                st.subheader("Risk Assessment")

                col_a, col_b = st.columns(2)

                with col_a:
                    st.metric(
                        "Risk Level",
                        data.get(
                            "risk_level",
                            "UNKNOWN"
                        )
                    )

                with col_b:
                    st.metric(
                        "Risk Score",
                        f"{data.get('risk_score', 0):.3f}"
                    )

                st.write(
                    "Top Factors:",
                    data.get(
                        "top_factors",
                        []
                    )
                )

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.json(response.json())

        except Exception as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )


# -------------------------------------------------
# Work Item Dashboard
# -------------------------------------------------

st.markdown("---")

st.header("📊 Work Item Dashboard")


col1, col2 = st.columns(2)


# -------------------------------------------------
# Get All Work Items
# -------------------------------------------------

with col1:

    if st.button(
        "📋 Get All Work Items",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{API_URL}/api/v1/work-items",
                timeout=30
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    f"Total Work Items: {len(data)}"
                )

                if data:
                    st.dataframe(
                        data,
                        use_container_width=True
                    )
                else:
                    st.info(
                        "No work items found."
                    )

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )


# -------------------------------------------------
# Prioritized Work Items
# -------------------------------------------------

with col2:

    if st.button(
        "🚨 Show Prioritized Queue",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{API_URL}/api/v1/work-items/prioritized",
                timeout=30
            )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    f"Prioritized Items: {len(data)}"
                )

                if data:

                    st.dataframe(
                        data,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No work items found."
                    )

            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

        except Exception as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )


# -------------------------------------------------
# Health Check
# -------------------------------------------------

st.markdown("---")

if st.button("💚 Check API Health"):

    try:

        response = requests.get(
            f"{API_URL}/api/v1/health",
            timeout=10
        )

        if response.status_code == 200:

            st.success(
                "FastAPI service is healthy!"
            )

            st.json(response.json())

        else:

            st.error(
                f"Health check failed: "
                f"{response.status_code}"
            )

    except Exception as e:

        st.error(
            f"Could not connect to FastAPI: {e}"
        )
