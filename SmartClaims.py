import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import StratifiedKFold

filepath = 'C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\Smart Claims Data.csv'

df = pd.read_csv(filepath, encoding='cp1252')
pd.set_option('display.max_columns', None)

df.drop(['Claim_ID', 'Customer_Phone', 'Customer_Email',
         'Incident_Date', 'Claim_Submission_Date',
         'Policy_Start_Date', 'Policy_End_Date'
        ], axis=1, inplace=True)

suspicious_claims = df[df['Claim_Amount'] > 251000]
#suspicious_claims

non_suspicious_claims = df[df['Claim_Amount'] < 250000]
#non_suspicious_claims

df.drop(['Customer_Name', 'Policy_Number', 'Adjuster_Notes'], axis=1, inplace=True)

numerical_columns = ['Claim_Amount', 'Customer_Age', 'Premium_Amount']
categorical_columns = ['Location', 'Policy_Type',
                       'Claim_Type', 'Incident_Type',
                       'Claim_Status', 'Customer_Gender',
                       'Customer_Occupation'
                       ]

df_model = df

y = df_model['Fraud_Flag']
X = df_model.drop(['Fraud_Flag'], axis=1)

print(X.shape)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=y)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# reshape the array as we are predicting for one instance
 #df_model.reshape(1,-1)

preprocessor = ColumnTransformer(
    transformers = [
        ('numerical', StandardScaler(), numerical_columns),
        ('categorical', OneHotEncoder(drop='first'), categorical_columns)
    ],
    remainder='passthrough'
)

pipeline = Pipeline([
    ('prep3', preprocessor),
    ('clf3', RandomForestClassifier(n_estimators=100, max_depth=3, criterion='entropy', random_state=42))
])

pipeline.fit(X_train, y_train)

rf_predict = pipeline.predict(X_test)
#rf_predict

print(classification_report(y_test, rf_predict))

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_score = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=-1)
print('Cross validation score:', cv_score)
print('Mean accuracy score:', cv_score.mean())

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from io import StringIO
import requests
import joblib
from streamlit_option_menu import option_menu
#from hooks import set_png_as_page_bg
import base64
import json
import requests
from fpdf import FPDF
import os

# Sidebar for Navigation
with st.sidebar:
 selected = option_menu(
 'Supporting Documentation',
 ['Methodology', 'How to use', 'CodeBase', 'Requirements'],
 icons=['activity', 'person', 'code', 'book'],
 default_index=0
 )

# Setting Page Configuration
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
            st.sidebar.success("Hurray! You have been registered. Please login.")
        else:
            st.sidebar.warning("Username already exists.")

filepath = 'C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\Smart Claims Data.csv'

df = pd.read_csv(filepath, encoding='cp1252')
pd.set_option('display.max_columns', None)
#df.head()

joblib.dump(pipeline, 'fraud_detection_model.pkl')

model = joblib.load('fraud_detection_model.pkl')

# Add widgets
image = Image.open('C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\axa-logo.png')
st.image(image, width=70)

BACKGROUND_IMAGE = 'C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\BACKGROUND4.jpg'
#set_jpg_as_page_bg(BACKGROUND_IMAGE)

'''def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local(BACKGROUND_IMAGE)'''

st.markdown('## AXA Mansard Insurance Plc')
st.markdown('##### Analyze insurance claims, detect fraud, simulate cost optimization and export reports')
st.markdown('##### Welcome! 👋')

# ---- MAIN APP ----
if auth_success:
# Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📊 Dashboard", "📥 Export Report", "📄 PDF Report Summary"])

#tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📊 Dashboard", "📥 Export Report", "📄 PDF Report Summary"])

st.markdown("""
        ####### Analyze insurance claims, detect fraud, simulate cost optimization and export reports.
        """)

'''st_lottie = st.components.v1.html(f"""
        <lottie-player src="https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json" background="transparent" speed="1" style="width: 400px; height: 400px;" loop autoplay></lottie-player>
        """, height=400)'''

with tab2:
    st.header("📊 Claim Analytics Dashboard")

'''st.subheader("Raw Data Preview")
st.dataframe(df.head())'''

'''st.markdown("#### Click the button below to upload your claims data")
df = pd.read_csv('Smart Claims Data.csv')
if st.button("Upload Claims Data"):
    st.text("Your data upload was successful!")
if st.button("Show Report"):
    report = st.write(df)
    st.success(report)'''

st.subheader("High Value Claim Detection")
threshold = df['Claim_Amount'].quantile(0.80)
high_claims = df[df['Claim_Amount'] > threshold]
st.write(f"Claims above 80th percentile (₹{threshold:.2f})")
#st.dataframe(high_claims)

st.subheader("Frequent Claimants")
frequent_claims = df['Customer_Name'].value_counts()
frequent_customers = frequent_claims[frequent_claims > 3]
st.write(f"Customers with greater than 3 claims: {len(frequent_customers)}")
st.dataframe(frequent_customers)

from scipy.stats import zscore
st.subheader("Z-Score Anomaly Detection")
df['z_score'] = zscore(df['Claim_Amount'])
anomalies = df[df['z_score'].abs() > 3]
st.write(f"Anomalous claims (Z > 3): {len(anomalies)}")
st.dataframe(anomalies)

st.subheader("Claim Amount Distribution")
fig, ax = plt.subplots()
sns.boxplot(x=df['Claim_Amount'], ax=ax)
#st.pyplot(fig)

if 'Claim_Type' in df.columns:
    st.subheader("Cost Center Analysis")
    dept_costs = df.groupby('Incident_Type')['Claim_Amount'].sum().sort_values(ascending=False)
    #st.bar_chart(dept_costs)

st.subheader("Simulated Claim Capitation")
df['capped_claim'] = np.where(df['Claim_Amount'] > 300000, 300000, df['Claim_Amount'])
savings = df['Claim_Amount'].sum() - df['capped_claim'].sum()
st.write(f"Total Savings with Cap: ₹{savings:,.2f}")

with tab3:
    st.header("📤 Export Data")
if st.button("Export to Excel"):
    df.to_excel("processed_insurance.xlsx", index=False)
with open("processed_insurance.xlsx", "rb") as file:
    b64 = base64.b64encode(file.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="processed_insurance.xlsx">📥 Download Excel</a>'
st.markdown(href, unsafe_allow_html=True)

# PDF Report Generator
def generate_pdf_report(data_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Claims Analysis Report", ln=True, align='C')
    pdf.ln(10)
    for line in data_summary:
        pdf.multi_cell(0, 10, line)
    filename = "Claims Report.pdf"
    pdf.output(filename)
    return filename

with tab4:
    st.header("📄 Generate PDF Report")
report_summary = [
    f"Total Claims: {len(df)}",
    f"High-Value Claims (>80th percentile): {len(high_claims)}",
    f"Frequent Patients (>5 claims): {len(frequent_customers)}",
    f"Anomalous Z-Score Claims: {len(anomalies)}",
    f"Total Savings after Cap: ₹{savings:,.2f}"
]

if st.button("Generate PDF Report"):
    pdf_file = generate_pdf_report(report_summary)
    with open(pdf_file, "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_file}">📄 Download Report</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Please login to access the dashboard.")

'''# Create the select boxes
location = st.selectbox('Location :', ['--Select--', 'Ibadan', 'Port Harcourt', 'Abuja', 'Kano', 'Lagos'])
claim_type = st.selectbox('Claim type :', ['--Select--', 'Gadget', 'Auto', 'Fire', 'Life', 'Health'])
policy_type = st.selectbox('Policy type :', ['--Select--', 'Corporate', 'Family', 'Individual'])
incident_type = st.selectbox('Incident type :', ['--Select--', 'Death', 'Theft', 'Fire', 'Accident', 'Illness'])'''

st.markdown("###### Claim Request Authorization")
approve_reject = st.selectbox('Approve or Reject claim requests :', ['--Select--', 'Approved',
                                                                     'Rejected', 'Denied', 'Flagged'])
comment = st.text_area('Comments (Reason for rejection) :')

policy_number = df['Policy_Number'].unique()
selected_id = st.selectbox(
    "Select or manually enter policy number (This criteria selects a row from the table) :",
    policy_number)
filtered_df = df[df['Policy_Number'] == selected_id]
st.write('Filtered claim data :')
st.dataframe(filtered_df)

# Add a slider for Age
min_age, max_age = int(df['Customer_Age'].min()), int(df['Customer_Age'].max())
age_range = st.slider("Select age range :", min_age, max_age, (min_age, max_age))
filtered_df_age = df[(df['Customer_Age'] >= age_range[0]) & (df['Customer_Age'] <= age_range[1])]
st.write('Filtered age data :')
st.dataframe(filtered_df_age)


'''uploaded_file = st.file_uploader("Choose a file to upload:")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)'''

'''selected_location = df[df['Location'] == location]
selected_claim_type = df[df['Claim_Type'] == claim_type]
selected_policy_type = df[df['Policy_Type'] == policy_type]
selected_incident_type = df[df['Incident_Type'] == incident_type]'''

# Show claims data for sorting and filtering
st.write("Click the button below to show uploaded claims data")
df = pd.read_csv(filepath)
if st.button("Show Claims Data"):
    report = st.write(df)

# Create hide data button
if "Show Claims Data" not in st.session_state:
    st.session_state.show_button = True
def hide_session_state():
    st.session_state.show_button = False
if st.session_state.show_button:
    st.button("Hide Claims Data", on_click=hide_session_state)
else:
    st.write("Hide Claims Data")

st.markdown("###### Select any option below to filter claims data")

# Filter claims data with select boxes
# Get unique options for each filter and add 'All'
location = ['--Select--'] + list(df['Location'].unique())
claim_type = ['--Select--'] + list(df['Claim_Type'].unique())
policy_type = ['--Select--'] + list(df['Policy_Type'].unique())
incident_type = ['--Select--'] + list(df['Incident_Type'].unique())

# Create the select boxes
selected_loc = st.selectbox("Location :", options=location) # change boxes names
selected_ct = st.selectbox("Claim type :", options=claim_type) # change boxes names
selected_pt = st.selectbox("Policy type :", options=policy_type) # change boxes names
selected_it = st.selectbox("Incident type :", options=incident_type) # change boxes names

# Creating filters
filtered_df = df.copy()
if selected_loc != '--Select--':
    filtered_df = filtered_df[filtered_df['Location'] == selected_loc]
if selected_ct != '--Select--':
    filtered_df = filtered_df[filtered_df['Claim_Type'] == selected_ct]
if selected_pt != '--Select--':
    filtered_df = filtered_df[filtered_df['Policy_Type'] == selected_pt]
if selected_it != '--Select--':
    filtered_df = filtered_df[filtered_df['Incident_Type'] == selected_it] # stopped here 3333333333333

'''st.write("Click the button below to show filtered claims data")
df = pd.read_csv(filepath)
if st.button("Show Filtered Claims Data"):
    report = st.write(filtered_df)''' # PENDING

st.write("Filtered claims data :")
st.dataframe(filtered_df)

'''st.write("Click the button below to show filtered claims data")
df = pd.read_csv(filepath)
if st.button("Show Filtered Claims Data"):
    report = st.write(df)''' # PENDING

if "Filtered claims data" not in st.session_state:
    st.session_state.show_button = True
def hide_session_state():
    st.session_state.show_button = False
if st.session_state.show_button:
    st.button("Hide Filtered Claims Data", on_click=hide_session_state)
else:
    st.write("Hide Filtered Claims Data")

claim_amount = st.number_input('Enter claim amount (₦)',
                               min_value=0.00,
                               value=0.00,
                               step=1.01,
                               format="%.2f")
st.write("The claim amount entered : (₦)", claim_amount)

prediction = model.predict(X_test)[0]
st.subheader(f"Prediction Result: '{int(prediction)}'")

pred_button = st.button('Predict Claim')
if pred_button:
    st.session_state.show_button = True
else:
    st.write(prediction)

if prediction == 1:
    st.error('Caution: This claim transaction look suspicious. Please, exercise due diligence.')
    st.success('Status: Flagged as suspicious transaction.')
else:
    st.success('This claim transaction passed credibility check. It is presumed good for approval and further processing.')
    st.success('Status: Passed credibility check.')

# EMAIL NOTIFICATION TO CUSTOMERS (TIMESTAMP)