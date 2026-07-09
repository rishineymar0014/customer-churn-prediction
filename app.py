import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Model
# -----------------------------
model_data = joblib.load("customer_churn_model.pkl")
model = model_data["model"]
feature_names = model_data["feature_names"]

encoders = joblib.load("encoders.pkl")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#F5F7FA;
}

.title{
    text-align:center;
    color:#0E4C92;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.stButton>button{
    width:100%;
    background:#0E4C92;
    color:white;
    height:55px;
    font-size:20px;
    border-radius:10px;
}

.result{
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='title'>📊 Customer Churn Prediction</div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Predict whether a customer is likely to leave the company.</div>", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Input Layout
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox("Gender", ["Male", "Female"])

    senior = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.slider(
        "Tenure (Months)",
        0,
        72,
        12
    )

    phone = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    internet = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

with col2:

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )

    device = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    tech = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )

    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly = st.number_input(
    "Monthly Charges",
    0.0,
    500.0,
    70.0
)

total = st.number_input(
    "Total Charges",
    0.0,
    10000.0,
    1000.0
)

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Churn"):

    data = {
        "gender": gender,
        "SeniorCitizen": 1 if senior=="Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device,
        "TechSupport": tech,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    df = pd.DataFrame([data])

    # Encode categorical columns
    for col in df.columns:
        if col in encoders:
            df[col] = encoders[col].transform(df[col])

    # Ensure column order
    df = df.reindex(columns=feature_names, fill_value=0)

    prediction = model.predict(df)[0]

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(df)[0][1] * 100
    else:
        probability = 0

    st.write("")

    if prediction == 1:
        st.error(
            f"⚠️ Customer is likely to Churn\n\nProbability: {probability:.2f}%"
        )
    else:
        st.success(
            f"✅ Customer is likely to Stay\n\nProbability of Churn: {probability:.2f}%"
        )