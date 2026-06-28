import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=200)

    if st.button("Analyze Resume"):

        response = model.generate_content(
            "Analyze this resume and provide:\n"
            "1. Resume Score out of 100\n"
            "2. ATS Score\n"
            "3. Skills Found\n"
            "4. Strengths\n"
            "5. Weaknesses\n"
            "6. Missing Skills\n"
            "7. Recommended Job Roles\n"
            "8. Interview Questions\n\n"
            + resume_text
        )

        st.write(response.text)

        st.download_button(
            label="Download Report",
            data=response.text,
            file_name="Resume_Report.txt",
            mime="text/plain"
        )