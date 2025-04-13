
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Cardiovascular Risk Analyzer", layout="centered")
st.title("❤️ Cardiovascular Risk Analyzer")
st.markdown("""
This app estimates your risk of cardiovascular disease based on your health profile.
""")

# Sidebar form
st.sidebar.header("Enter Your Health Info")
age = st.sidebar.slider("Age", 20, 80, 30)
gender = st.sidebar.radio("Gender", ["Male", "Female"])
systolic_bp = st.sidebar.slider("Systolic Blood Pressure (mm Hg)", 90, 200, 120)
diastolic_bp = st.sidebar.slider("Diastolic Blood Pressure (mm Hg)", 60, 120, 80)
cholesterol = st.sidebar.slider("Cholesterol (mg/dL)", 100, 400, 200)
glucose = st.sidebar.slider("Glucose (mg/dL)", 70, 200, 100)
bmi = st.sidebar.slider("BMI", 15.0, 45.0, 22.0)
smoker = st.sidebar.selectbox("Do you smoke?", ["No", "Yes"])
diabetic = st.sidebar.selectbox("Diabetic?", ["No", "Yes"])

if st.sidebar.button("Calculate Risk"):
    # Dummy logic for risk (replace with model prediction)
    risk_score = (age - 20) * 0.5 + (1 if smoker == "Yes" else 0)*10 + (1 if diabetic == "Yes" else 0)*10
    risk_score += (cholesterol - 200) * 0.05 + (systolic_bp - 120) * 0.1
    risk_score += (bmi - 22) * 0.4
    risk_score = min(max(risk_score, 0), 100)

    # Risk level color
    if risk_score < 25:
        risk_level = "Low"
        color = "green"
    elif risk_score < 60:
        risk_level = "Moderate"
        color = "orange"
    else:
        risk_level = "High"
        color = "red"

    # Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        delta = {'reference': 50},
        title = {'text': f"Risk Score: {risk_level}", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 25], 'color': 'lightgreen'},
                {'range': [25, 60], 'color': 'gold'},
                {'range': [60, 100], 'color': 'salmon'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_score}
        }))
    st.plotly_chart(fig)

    # Summary
    st.subheader("📋 Health Summary")
    st.markdown(f"**Your estimated cardiovascular risk is:** {risk_score:.2f}% ({risk_level} Risk)")

    st.subheader("📈 Comparison With Normal Ranges")
    comp_data = pd.DataFrame({
        'Category': ['Cholesterol', 'Glucose', 'BMI', 'Systolic BP'],
        'Your Value': [cholesterol, glucose, bmi, systolic_bp],
        'Recommended Max': [200, 100, 24.9, 120]
    })
    st.bar_chart(comp_data.set_index('Category'))

    # Suggestions
    st.subheader("💡 Health Suggestions")
    if risk_score < 25:
        st.success("Keep up the good work! Maintain a healthy lifestyle.")
    else:
        if smoker == "Yes":
            st.warning("🚭 Consider quitting smoking to lower your risk.")
        if diabetic == "Yes":
            st.warning("🍬 Control blood sugar levels through diet and medication.")
        if cholesterol > 200:
            st.warning("🥗 Eat a heart-healthy diet to reduce cholesterol.")
        if systolic_bp > 120:
            st.warning("🧘‍♀️ Practice relaxation and monitor blood pressure.")
        if bmi > 25:
            st.warning("🏃‍♂️ Aim for regular physical activity to manage weight.")

    # Download option
    st.download_button("📥 Download Report", f"Your risk score: {risk_score:.2f}% ({risk_level})", file_name="risk_report.txt")

else:
    st.info("Fill in the information and press **Calculate Risk** to see results.")
