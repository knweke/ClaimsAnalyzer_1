altair==5.4.1
attrs==24.2.0
blinker==1.8.2
cachetools==5.5.0
certifi==2024.8.30
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
contourpy==1.3.0
cycler==0.12.1
fonttools==4.54.0
gitdb==4.0.11
GitPython==3.1.43
idna==3.10
Jinja2==3.1.4
joblib==1.4.2
jsonschema==4.23.0
jsonschema-specifications==2023.12.1
kiwisolver==1.4.7
markdown-it-py==3.0.0
MarkupSafe==2.1.5
matplotlib==3.9.2
mdurl==0.1.2
narwhals==1.8.2
numpy==2.1.1
packaging==24.1
pandas==2.2.3
patsy==0.5.6
pillow==10.4.0
protobuf==5.28.2
pyarrow==17.0.0
pydeck==0.9.1
Pygments==2.18.0
pyparsing==3.1.4
python-dateutil==2.9.0.post0
pytz==2024.2
referencing==0.35.1
requests==2.32.3
rich==13.8.1
rpds-py==0.20.0
scikit-learn==1.5.2
scipy==1.14.1
seaborn==0.13.2
six==1.16.0
smmap==5.0.1
statsmodels==0.14.3
streamlit==1.38.0
tenacity==8.5.0
threadpoolctl==3.5.0
toml==0.10.2
tornado==6.4.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
watchdog==4.0.2
xgboost==2.1.1

# Display content based on menu selection
if selected == "Methodology":
    st.markdown("##### Methodology")
    st.write(
        '''
        Claims Fraud Detection Using Machine Learning
        
        - Introduction
        Due to the increase in the number of insurance claims in the recent past, it has become an important challenge for the insurance companies to identify the fraudulent claims. 
        Fraudulent claims can result in significant financial losses, and detecting them manually is time-consuming and prone to errors. 
        Therefore, the use of machine learning models to automate and enhance fraud detection has gained popularity.
        
        In this project, we have implemented an ML solution pipeline from scratch which is used to classify an insurance claim as either fraudulent or not. 
        We analyzed, cleaned, and tested several machine learning techniques to build a reliable fraud detection system. 
        The idea is to enhance the likelihood of the insurance companies to identify fraudulent claims and thereby minimize their losses and optimize their performance.
        
        - Problem Statement
        The primary objective of this project is to develop a predictive model that can identify fraudulent claims from a dataset containing various claim and patient-related features. 
        Specifically, we aim to answer the following questions:
        
        Can we accurately predict whether an insurance claim is fraudulent using machine learning techniques?
        What are the most influential factors in identifying fraudulent claims?
        How can we improve the model’s performance using hyperparameter tuning?
        
        - Data Collection
        The data used in this project was sourced from the Kaggle Medicare Fraud Detection dataset. 
        The dataset contains features related to the provider, reimbursement amounts, chronic conditions, and patient demographics. 
        The target variable indicates whether a claim is fraudulent or not.
        
        Methodology
        - Exploratory Data Analysis (EDA)
        In the EDA phase, we analyzed the distribution of key variables and their relationships to the target variable (fraud). 
        This included:
        
        Visualizing Data Distributions: Histograms, box plots, and density plots were used to observe the distribution of variables such as claim amounts, provider codes, and chronic conditions.
        Correlation Analysis: A correlation matrix helped identify the relationships between features and the target variable.
        Fraud Pattern Analysis: We analyzed the patterns of fraudulent claims across demographic groups and reimbursement amounts.
        
        - Model Building
        We developed several machine learning models to predict claim fraud:
        
        Logistic Regression: A simple linear model to serve as a baseline.
        
        Random Forest Classifier: A powerful ensemble model that creates multiple decision trees to improve prediction accuracy.
        
        Support Vector Machine (SVM): Used to find the optimal hyperplane that maximizes the margin between the fraud and non-fraud claims.
        
        XGBoost: A gradient-boosted tree-based algorithm known for its speed and performance.
        
        Each model was evaluated based on its ability to handle class imbalance, as the number of non-fraudulent claims far exceeded the fraudulent ones. 
        Metrics such as accuracy, precision, recall, and F1-score were calculated for each model.
        
        - Hyperparameter Tuning
        To further improve the performance of our models, we implemented hyperparameter tuning using GridSearchCV. 
        This allowed us to find the best combination of hyperparameters for each model. For example:
        
        In Random Forest, we tuned the number of trees (n_estimators) and the depth of trees (max_depth).
        For XGBoost, we tuned the learning rate (eta), maximum depth, and the number of boosting rounds.
        After hyperparameter tuning, the best-performing model was selected for deployment.
        
        - Model Evaluation
        The final models were evaluated using a hold-out test dataset to ensure that they generalized well to unseen data. 
        The evaluation metrics included:
        
        Accuracy: Proportion of correct predictions.
        Precision: Percentage of correctly predicted fraudulent claims out of all predicted fraudulent claims.
        Recall: Percentage of correctly predicted fraudulent claims out of all actual fraudulent claims.
        F1-Score: A harmonic mean of precision and recall to balance false positives and false negatives.
        The Gradient Boosting using GridSearchCV model performed the best, achieving a recall score of 97%, which is crucial in fraud detection tasks where it is essential to minimize false negatives (i.e., missing fraudulent claims). 
        The model also achieved a descent accuracy, striking a good balance between precision and recall
        
        - Model Deployment
        The selected Random Forest model was deployed using Streamlit, a Python framework that allows for rapid web application development. 
        The deployment process involved the following steps:
        
        Saving the Model: The best-performing model was saved as a claims_fraud_detection.pkl file using Joblib.
        Building the Streamlit Web App: An intuitive web interface was created using Streamlit, where users can input claim details and get a prediction of whether the claim is fraudulent.
        Launching the Web App: The app was deployed to the web, allowing real-time interaction with the model via the web interface.
        The Streamlit app is user-friendly and allows insurance companies to input relevant claim data and receive instant fraud predictions. 
        The interactive interface also includes easy-to-use drop-down menus and number input fields for claim details such as demographics, claim amount, and other variables used for claims processing.
        
        In this project, we successfully built and deployed a machine learning solution to detect fraudulent insurance claims. 
        Using multiple models, hyperparameter tuning, and advanced techniques for handling class imbalance, we were able to develop a high-performing system. 
        This solution can assist insurance companies in reducing fraud and improving claim processing efficiency.
        
        The final solution was deployed as a Streamlit web application, enabling real-time interaction and predictions, which makes the model highly accessible to stakeholders and end users.
        '''
    )


import streamlit as st

st.title('How to Use')
how_to_use = st.write(
"""
To use the Insurance Fraud Detection system, follow these steps:

- Open the Streamlit application.

- Login or sign up to access the App's predictive functionality, metrics and reports.

- Upload the claims dataset which will be used for filtering and predictive analysis.

- Select the input parameters to filter claims data.

- Click the "Show Prediction Result" button to get the fraud detection prediction result.

- Initiate authorizations and other operations that leverage API services.

- Submit pre-authorized claim for further processing.

""")
