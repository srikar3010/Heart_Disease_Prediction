import streamlit as st
import numpy as np
import pickle

# Load model
with open('heart_disease_models.pkl', 'rb') as f:
    model = pickle.load(f)

# Set page background image using CSS
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1576765607924-7a13158e7c70?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.stButton>button {
    display: block;
    margin: 0 auto;
    width: 200px;
    background-color: #e63946;
    color: white;
    font-weight: bold;
}
h1 {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Set centered heading
st.markdown("<h1 style='text-align: center;'>Heart Disease Prediction</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
with col2:
    sex = st.selectbox("Sex", options=["Male", "Female"])

col3, col4 = st.columns(2)
with col3:
    cp = st.selectbox("Chest Pain Type", options=[
        "Typical Angina",
        "Atypical Angina",
        "Non-anginal Pain",
        "Asymptomatic"
    ])
with col4:
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120)

col5, col6 = st.columns(2)
with col5:
    chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
with col6:
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["No", "Yes"])

col7, col8 = st.columns(2)
with col7:
    restecg = st.selectbox("Resting Electrocardiographic Results", options=[
        "Normal",
        "ST-T Wave Abnormality",
        "Left Ventricular Hypertrophy"
    ])
with col8:
    thalach = st.number_input("Max Heart Rate Achieved", min_value=60, max_value=220, value=150)

col9, col10 = st.columns(2)
with col9:
    exang = st.selectbox("Exercise Induced Angina", options=["No", "Yes"])
with col10:
    oldpeak = st.number_input("ST Depression Induced by Exercise (oldpeak)", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

col11, col12 = st.columns(2)
with col11:
    slope = st.selectbox("Slope of Peak Exercise ST Segment", options=[
        "Upsloping",
        "Flat",
        "Downsloping"
    ])
with col12:
    ca = st.number_input("Number of Major Vessels Colored by Fluoroscopy (0-3)", min_value=0, max_value=3, value=0)

# Full width for last attribute
thal = st.selectbox("Thalassemia", options=[
    "Normal",
    "Fixed Defect",
    "Reversible Defect"
])

# Encode categorical variables
sex_val = 1 if sex == "Male" else 0
cp_mapping = {
    "Typical Angina": 0,
    "Atypical Angina": 1,
    "Non-anginal Pain": 2,
    "Asymptomatic": 3
}
cp_val = cp_mapping[cp]
fbs_val = 1 if fbs == "Yes" else 0
restecg_mapping = {
    "Normal": 0,
    "ST-T Wave Abnormality": 1,
    "Left Ventricular Hypertrophy": 2
}
restecg_val = restecg_mapping[restecg]
exang_val = 1 if exang == "Yes" else 0
slope_mapping = {
    "Upsloping": 0,
    "Flat": 1,
    "Downsloping": 2
}
slope_val = slope_mapping[slope]
thal_mapping = {
    "Normal": 1,
    "Fixed Defect": 2,
    "Reversible Defect": 3
}
thal_val = thal_mapping[thal]

input_data = np.array([[age, sex_val, cp_val, trestbps, chol, fbs_val,
                        restecg_val, thalach, exang_val, oldpeak,
                        slope_val, ca, thal_val]])

if st.button("Predict"):
    prediction = model.predict(input_data)
    if prediction[0] == 0:
        st.success("No Heart Disease Detected")
    else:
        st.error("Heart Disease Detected — Please Consult a Doctor")
