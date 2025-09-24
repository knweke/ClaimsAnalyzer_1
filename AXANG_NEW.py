import streamlit as st
import streamlit_authenticator as stauth
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from io import StringIO
import requests
#from scipy.stats import zscore
from streamlit_option_menu import option_menu
import base64
import json
#from fpdf import FPDF
import os
#from xgboost.testing.data import joblib
#from ClaimsAppModel import pipeline
from streamlit_authenticator import Hasher
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

# https://pypi.org/project/streamlit-authenticator/

# --- Configuration for Sign-Up and Email ---
# Use a separate YAML file for credentials in production
# For simplicity, we'll keep it in memory for this example
# In a real app, you would load and save this to a file or database

# Add widgets
image = Image.open('C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\axa-logo.png')
st.image(image, width=80)

st.markdown('<p style="font-family: calibri; color:#000080; font-size: 38px;">AXA Mansard Insurance Plc</p>', unsafe_allow_html=True)
# st.markdown('## AXA Mansard Insurance Plc')
st.markdown("##### Life and Non-Life Insurance Claims Analyzer and Anomaly Detector")

image2 = Image.open('C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\insight-logo3.png')
st.image(image2, width=150)

# Set background image
BACKGROUND_IMAGE = 'C:\\Users\\Springrose\\Downloads\\FRAUD DETECTION\\BACKGROUND2.png'

def add_bg_from_local(image_file):
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
add_bg_from_local(BACKGROUND_IMAGE)

with open('C:/Users/Springrose/PyCharmMiscProject/user_cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

USER_CREDENTIALS = {
    'usernames': {
        'admin': {
            'email': 'admin@axamansard.com',
            'name': 'Admin',
            'is_email_verified': True
        }
    }
}

AUTHENTICATOR = stauth.Authenticate(
    USER_CREDENTIALS,
    'my_app_cookie',
    'my_app_key',
    cookie_expiry_days=30
)

try:
    AUTHENTICATOR.login()
except Exception as e:
    st.error(e)

# Email configuration (replace with your actual details)
SMTP_SERVER = 'smtp.axamansard.com'  # Example for Gmail
SMTP_PORT = 587
SENDER_EMAIL = 'knweke@axamansard.com'
SENDER_PASSWORD = 'abc'  # Use an app-specific password, not your account password
REQUIRED_DOMAIN = "@axamansard.com"

# --- Email Sending Logic ---
def send_email_confirmation(receiver_email, token):
    """Sends an email with a confirmation link."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject:"] = "Confirm your email address"
        msg["From:"] = SENDER_EMAIL
        msg["To:"] = receiver_email

        # In a real app, this link would point to a page that confirms the email
        # The token would be stored temporarily in a database
        confirmation_link = f"http://localhost:8501/?token={token}"
        html = f"""\
            <html>
              <body>
                <p>Hi there,<br>
                   Please click the link below to confirm your email address and activate your account:<br>
                   <a href="{confirmation_link}">Confirm Email</a>
                </p>
              </body>
            </html>
            """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# --- App Layout and Logic ---
st.title("Streamlit User Authentication")

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# Sidebar for navigation
with st.sidebar:
    st.sidebar.title("🔐 User Authentication")
    page = st.radio("Choose Action:", ["Login", "Sign Up"])

# Main content
if st.session_state['authentication_status']:
    # Protected content for logged-in users
    st.write(f"Welcome, {st.session_state['name']}!")
    st.write("This is the protected content of your app.")
    AUTHENTICATOR.logout('Logout', 'sidebar')

'''elif page == "Login":
    # Login page
    st.header("Login")
    name, authentication_status, username = AUTHENTICATOR.login('Login', 'main')
    st.write(f"Welcome, {name}!")

    if authentication_status:
        st.session_state['name'] = name
        st.session_state['authentication_status'] = True
        st.session_state['username'] = username
        st.rerun()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.info('Please enter your username and password')'''

#hashed_passwords = stauth.Hasher(['abc']).generate_hash()
#stauth.Hasher.hash_passwords(config['credentials'])

'''# 'password': stauth.Hasher(['secret']).generate_hash(),
USER_CREDENTIALS = {
    'usernames': {
        'admin': {
            'email': 'admin@axamansard.com',
            'name': 'Admin',
            'is_email_verified': True
        }
    }
}

# Hashing individual passwords
#passwords_to_hash = ['password1', 'password2']
#hashed_passwords = [Hasher().hash(password) for password in passwords_to_hash]
##st.write(hashed_passwords)

AUTHENTICATOR = stauth.Authenticate(
    USER_CREDENTIALS,
    'my_app_cookie',
    'my_app_key',
    cookie_expiry_days=30
)

# Email configuration (replace with your actual details)
SMTP_SERVER = 'smtp.gmail.com'  # Example for Gmail
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_app_password'  # Use an app-specific password, not your account password
REQUIRED_DOMAIN = "@axamansard.com"

# --- Email Sending Logic ---
def send_email_confirmation(receiver_email, token):
    """Sends an email with a confirmation link."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject:"] = "Confirm your email address"
        msg["From:"] = SENDER_EMAIL
        msg["To:"] = receiver_email

        # In a real app, this link would point to a page that confirms the email
        # The token would be stored temporarily in a database
        confirmation_link = f"http://localhost:8501/?token={token}"
        html = f"""\
        <html>
          <body>
            <p>Hi there,<br>
               Please click the link below to confirm your email address and activate your account:<br>
               <a href="{confirmation_link}">Confirm Email</a>
            </p>
          </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# --- App Layout and Logic ---
st.title("Streamlit User Authentication")

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Login", "Sign Up"])

# Main content
if st.session_state['authentication_status']:
    # Protected content for logged-in users
    st.write(f"Welcome, {st.session_state['name']}!")
    st.write("This is the protected content of your app.")
    AUTHENTICATOR.logout('Logout', 'sidebar')

elif page == "Login":
    # Login page
    st.header("Login")
    name, authentication_status, username = AUTHENTICATOR.login('Login', 'main')
    st.write(f"Welcome, {name}!")

    if authentication_status:
        st.session_state['name'] = name
        st.session_state['authentication_status'] = True
        st.session_state['username'] = username
        st.rerun()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.info('Please enter your username and password')

elif page == "Sign Up":
    # Sign-up page with domain validation
    st.header("Create a new account")
    try:
        email = st.text_input("Email", key="register_email")
        if email and not email.endswith(REQUIRED_DOMAIN):
            st.error(f"Please use an email address with the domain {REQUIRED_DOMAIN}.")
        else:
            # Only show the registration form if the email domain is valid
            # The register_user function will be triggered after the form is submitted
            if AUTHENTICATOR.register_user('Register'):
                token = secrets.token_urlsafe(16)  # Generate a secure token

                if send_email_confirmation(email, token):
                    st.success(
                        "Registration successful! A confirmation email has been sent. Please click the link to activate your account.")
                else:
                    st.error("Registration was successful, but the confirmation email could not be sent.")
    except Exception as e:
        st.error(e)'''