import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from app.chain import Chain
from app.portfolio import Portfolio
from app.utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # Page configuration
    st.set_page_config(
        page_title="📧 Cold Email Generator",
        page_icon="📧",
        layout="wide"
    )
    
    # Sidebar for inputs
    st.sidebar.header("🔧 Input Settings")
    input_choice = st.sidebar.radio("Choose Input Type:", ["Job URL", "Paste Job Description"])
    
    url_input = ""
    jd_input = ""
    if input_choice == "Job URL":
        url_input = st.sidebar.text_input("Enter a Job URL:", value="https://jobs.nike.com/job/R-33460")
    else:
        jd_input = st.sidebar.text_area("Paste the Job Description here:", value="Job Description – Generative AI / LLM Engineer: Seeking a talented Generative AI Engineer (1–4 yrs) to design, build, and optimize AI-driven solutions using LLMs, NLP pipelines, and intelligent automation; responsibilities include developing LLM-based applications (chatbots, document intelligence), implementing RAG pipelines with vector databases, fine-tuning open-source/proprietary models (Llama, Mistral, Falcon, GPT), creating FastAPI/Flask microservices for deployment, maintaining MLOps workflows with CI/CD and cloud, performing prompt engineering and evaluation, and working on multimodal AI; required skills: Python, NLP/LLMs, Transformers, Hugging Face, LangChain/LlamaIndex, vector DBs (Pinecone, FAISS, Chroma), Docker, Git, Linux, cloud (AWS/GCP/Azure); nice-to-have: CV/Speech AI, inference optimization (quantization, ONNX, vLLM), FastAPI+Gradio demos, Kubernetes, CI/CD; soft skills: communication, analytical thinking, ownership, teamwork; education: CS/AI/DS degree or equivalent; Location: Remote/Hybrid/On-site; Full-time role in fast-paced environment with innovation focus.", height=200)
    
    max_emails = st.sidebar.slider("Number of Emails to Generate", 1, 5, 1)
    submit_button = st.sidebar.button("Generate Email")
    
    # Main content
    st.title("📧 Cold Email Generator")
    st.markdown("""
        Welcome! This app extracts job requirements from a URL or a pasted Job Description, 
        matches your portfolio skills, and generates a professional cold email tailored for the role.
    """)

    if submit_button:
        with st.spinner("Processing... ⏳"):
            try:
                # Determine data source
                if input_choice == "Job URL":
                    if not url_input.strip():
                        st.error("Please enter a valid URL.")
                        return
                    loader = WebBaseLoader([url_input])
                    page_content = loader.load().pop().page_content
                    data = clean_text(page_content)
                else:
                    if not jd_input.strip():
                        st.error("Please paste a valid Job Description.")
                        return
                    data = clean_text(jd_input)
                
                # Load portfolio once
                portfolio.load_portfolio()
                
                # Extract jobs and generate emails
                jobs = llm.extract_jobs(data)
                
                if not jobs:
                    st.warning("No jobs found in the provided input.")
                
                for _ in range(max_emails):
                    for job in jobs:
                        
                        # st.subheader(f"💼 Job {i+1}: {job.get('title', 'Unknown Title')}")
                        
                        # Show job description
                        with st.expander("Job Description"):
                            st.write(job.get('description', 'No description available.'))
                        
                        # Show required skills
                        skills = job.get('skills', [])
                        # Match portfolio links
                        links = portfolio.query_links(skills)
                        
                        # Generate email
                        email = llm.write_mail(job, links)
                        st.markdown("**Generated Cold Email:**")
                        st.code(email, language='markdown')
                        
                        st.markdown("---")
                        break
            
            except Exception as e:
                st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
    
    
# python -m streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0

