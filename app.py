import streamlit as st
import numpy as np

# Increase the font size for the entire page
st.markdown(
    """
    <style>
    .reportview-container {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Set page config for layout and title
st.set_page_config(page_title="The cf-mtDNA Prognostic Score Calculator", layout="centered")
st.title("The cf-mtDNA-based Prognostic Score for HBV-ACLF")

# Markdown text with the formula
st.markdown("""
This tool calculates the **cf-mtDNA-based prognostic score** for predicting short-term mortality in HBV-related ACLF patients.

**Formula:**

> **Score =** 1.424 × log10(cf-mtDNA) + 0.702 × ln(TB) + 0.492 × ln(Creatinine) + 1.655 × ln(INR) + 0.487 × HE Score  

Where HE Score = 1 (none), 2 (grade I-II), 3 (grade III-IV)
""")

# Inputs for the user
mtDNA = st.number_input("cf-mtDNA (copies/μL)", min_value=100.0, step=100.0)
tb = st.number_input("Total Bilirubin (μmol/L)", min_value=1.0, step=1.0)
creatinine = st.number_input("Creatinine (μmol/L)", min_value=10.0, step=1.0)
inr = st.number_input("INR", min_value=0.5, step=0.1)
he_score = st.selectbox("Hepatic Encephalopathy (HE) Grade", options=["None (0)", "Grade I-II (1)", "Grade III-IV (2)"])

# Mapping HE score to numeric values
he_numeric = {"None (0)": 1, "Grade I-II (1)": 2, "Grade III-IV (2)": 3}[he_score]

# Calculate prognostic score when the button is pressed
if st.button("Calculate Prognostic Score"):
    try:
        # Calculate the prognostic score based on the input values
        score = (
            1.424 * np.log10(mtDNA)
            + 0.702 * np.log(tb)
            + 0.492 * np.log(creatinine)
            + 1.655 * np.log(inr)
            + 0.487 * he_numeric
        )
        
        # Output the result, making the prognostic score bold
        st.markdown(f"### **Prognostic Score: {score:.2f}**")

        # Check if the score indicates high or low risk
        if score >= 13.7:
            st.error("High-risk group: predicted low short-term survival")
        else:
            st.info("Low-risk group: predicted better short-term survival")
    
    except Exception as e:
        st.warning(f"Error in calculation: {e}")
