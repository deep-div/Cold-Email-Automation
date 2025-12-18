import streamlit as st
import requests

st.set_page_config(page_title="📧 Cold Email Generator", page_icon="📧", layout="wide")

st.sidebar.header("🔧 Input Settings")
input_choice = st.sidebar.radio("Choose Input Type:", ["Job URL", "Paste Job Description"])

url_input = ""
jd_input = ""
if input_choice == "Job URL":
    url_input = st.sidebar.text_input("Enter a Job URL:", value="https://jobs.nike.com/job/R-33460")
else:
    jd_input = st.sidebar.text_area("Paste the Job Description here:", value="MAQ Software is hiring a Technical Recruiter (1–4 yrs exp) for our Talent Acquisition team in Sector 145, Noida (next to Aqua Metro line); role involves full-cycle IT sourcing via Naukri/LinkedIn/referrals, pipeline building for niche roles (AI/ML, Python, Power BI, Azure), delivering excellent candidate experience, and partnering with hiring managers; requires strong tech stack understanding (Cloud, Full-Stack, Data), high ownership, proactive attitude, and comfort with a 6-day work week (Mon–Sat).", height=200)

max_emails = st.sidebar.slider("Number of Emails to Generate", 1, 5, 1)
submit_button = st.sidebar.button("Generate Email")

st.title("📧 Cold Email Generator")
st.markdown("This app sends your job input to the backend API and returns generated cold emails.")

if submit_button:
    with st.spinner("Processing... ⏳"):
        input_value = url_input if input_choice == "Job URL" else jd_input
        payload = {
            "input_type": input_choice,
            "input_value": input_value,
            "max_emails": max_emails
        }
        try:
            response = requests.post("http://localhost:8000/generate-email", json=payload)
            data = response.json()

            if "error" in data:
                st.error(data["error"])
            elif "warning" in data:
                st.warning(data["warning"])
            else:
                for idx, email_data in enumerate(data["emails"], 1):
                    with st.expander("Job Description"):
                        st.write(email_data["job_description"])
                    st.markdown("**Generated Cold Email:**")
                    st.code(email_data["email"], language="markdown")
                    st.markdown("---")
        except Exception as e:
            st.error(f"API Error: {e}")

# py -m streamlit run frontend/main.py