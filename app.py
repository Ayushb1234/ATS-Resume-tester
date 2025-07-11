import os
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

import streamlit as st
from extract_text import extract_text_from_pdf, extract_text_from_docx
from matcher import get_match_score, extract_keywords_from_job_desc

st.set_page_config(page_title="🎯 Job Fit Predictor", layout="centered")
st.title("🎯 AI-Powered Job Fit Predictor")
st.markdown("Upload your resume and a specific job description to calculate your **personalized match score** based on semantic similarity using BERT.")

# Upload Resume
uploaded_resume = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

job_input_type = st.radio("📝 Provide Job Description", ["Paste it here", "Upload (.txt or .docx)"])

job_desc = ""
if job_input_type == "Paste it here":
    job_desc = st.text_area("Paste the job description here:")
else:
    job_file = st.file_uploader("Upload Job Description File", type=["txt", "docx"])
    if job_file:
        if job_file.name.endswith(".txt"):
            job_desc = job_file.read().decode("utf-8")
        elif job_file.name.endswith(".docx"):
            job_desc = extract_text_from_docx(job_file)

# Resume and JD both provided
if uploaded_resume and job_desc:
    save_path = os.path.join("jobsaved", uploaded_resume.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_resume.getbuffer())

    ext = uploaded_resume.name.split(".")[-1]
    resume_text = extract_text_from_pdf(save_path) if ext == "pdf" else extract_text_from_docx(save_path)

    with st.spinner("🔍 Matching resume with job description..."):
        match_score = get_match_score(resume_text, job_desc)

    st.subheader("✅ Match Result")
    st.metric("Match Score", f"{match_score * 100:.2f}%")
    st.progress(min(match_score, 1.0))
    
    keywords = extract_keywords_from_job_desc(job_desc)

    st.markdown("### 🔑 Relevant Keywords in Job Description")
    st.markdown("These are important terms that should be reflected in your resume to increase match:")
    st.write(", ".join(keywords))

elif uploaded_resume or job_desc:
    st.info("ℹ️ Please upload both resume and job description.")
