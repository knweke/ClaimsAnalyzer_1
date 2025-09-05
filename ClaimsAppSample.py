import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import base64
import json
import requests
from fpdf import FPDF
import os

# ---- Page Config ----
st.set_page_config(page_title="Insurance Claims Analyzer", layout="wide", page_icon="💰")

# ---- Load Data ----
@st.cache_data
def load_data():
    return pd.read_csv("insurance.csv")

# ---- User Auth (CSV-based) ----
def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    # Load existing users or create a new DataFrame if file doesn't exist
    try:
        users = pd.read_csv("users.csv")
    except FileNotFoundError:
        users = pd.DataFrame(columns=["username", "password"])

    # Create a new row as a DataFrame
    new_user = pd.DataFrame([{"username": username, "password": password}])

    # ✅ Concatenate the new user row
    users = pd.concat([users, new_user], ignore_index=True)

    # Save the updated users list back to CSV
    users.to_csv("users.csv", index=False)
    return True


# ---- PDF Generator ----
def generate_pdf_report(data_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Insurance Claims Analysis Report", ln=True, align='C')
    pdf.ln(10)
    for line in data_summary:
        pdf.multi_cell(0, 10, line)
    filename = "insurance_report.pdf"
    pdf.output(filename)
    return filename

# ---- Sidebar: Login/Register ----
st.sidebar.title("🔐 User Authentication")

users_df = load_users()
auth_mode = st.sidebar.radio("Choose Action", ["Login", "Register"])
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

auth_success = False
if auth_mode == "Login":
    if st.sidebar.button("Login"):
        if username in users_df["username"].values:
            user_row = users_df[users_df["username"] == username]
            if user_row["password"].values[0] == password:
                auth_success = True
            else:
                st.sidebar.error("Incorrect password.")
        else:
            st.sidebar.warning("User not found.")
else:
    if st.sidebar.button("Register"):
        if save_user(username, password):
            st.sidebar.success("Registered! Please login.")
        else:
            st.sidebar.warning("Username already exists.")

# ---- MAIN APP ----
if auth_success:
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📊 Dashboard", "📥 Export", "📄 PDF Report"])

    with tab1:
        st.title("💡 Healthcare Insurance Claims Analyzer")
        st.write("Welcome **" + username + "**!")
        st.markdown("""
        Analyze medical insurance claims, detect fraud, simulate cost optimization and export reports.
        """)
        st_lottie = st.components.v1.html(f"""
        <lottie-player src="https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json" background="transparent" speed="1" style="width: 400px; height: 400px;" loop autoplay></lottie-player>
        """, height=400)

    with tab2:
        st.header("📊 Claim Analytics Dashboard")

        df = load_data()
        st.subheader("1. Raw Data Preview")
        st.dataframe(df.head())

        st.subheader("2. High-Value Claim Detection")
        threshold = df['claim_amount'].quantile(0.99)
        high_claims = df[df['claim_amount'] > threshold]
        st.write(f"Claims above 99th percentile (₹{threshold:.2f})")
        st.dataframe(high_claims)

        st.subheader("3. Frequent Claimants")
        frequent_claims = df['patient_id'].value_counts()
        frequent_patients = frequent_claims[frequent_claims > 10]
        st.write(f"Patients with >10 claims: {len(frequent_patients)}")
        st.dataframe(frequent_patients)

        st.subheader("4. Z-Score Anomaly Detection")
        df['z_score'] = zscore(df['charges'])
        anomalies = df[df['z_score'].abs() > 3]
        st.write(f"Anomalous claims (Z > 3): {len(anomalies)}")
        st.dataframe(anomalies)

        st.subheader("5. Claim Amount Distribution")
        fig, ax = plt.subplots()
        sns.boxplot(x=df['charges'], ax=ax)
        st.pyplot(fig)

        if 'department' in df.columns:
            st.subheader("6. Cost Center Analysis")
            dept_costs = df.groupby('smoker')['charges'].sum().sort_values(ascending=False)
            st.bar_chart(dept_costs)

        st.subheader("7. Simulate ₹10,000 Claim Cap")
        df['capped_claim'] = np.where(df['charges'] > 10000, 10000, df['charges'])
        savings = df['charges'].sum() - df['capped_claim'].sum()
        st.write(f"Total Savings with Cap: ₹{savings:,.2f}")

    with tab3:
        st.header("📤 Export Data")
        if st.button("Export to Excel"):
            df.to_excel("processed_insurance.xlsx", index=False)
            with open("processed_insurance.xlsx", "rb") as file:
                b64 = base64.b64encode(file.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="processed_insurance.xlsx">📥 Download Excel</a>'
                st.markdown(href, unsafe_allow_html=True)

    with tab4:
        st.header("📄 Generate PDF Report")
        summary = [
            f"Total Claims: {len(df)}",
            f"High-Value Claims (>99th percentile): {len(high_claims)}",
            f"Frequent Patients (>10 claims): {len(frequent_patients)}",
            f"Anomalous Z-Score Claims: {len(anomalies)}",
            f"Total Savings after Cap: ₹{savings:,.2f}"
        ]
        if st.button("Generate PDF"):
            pdf_file = generate_pdf_report(summary)
            with open(pdf_file, "rb") as file:
                b64 = base64.b64encode(file.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_file}">📄 Download Report</a>'
                st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Please login to access the dashboard.")