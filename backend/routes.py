from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from backend.chain import Chain
from backend.portfolio import Portfolio
from backend.utils import clean_text
from backend.logs.logger import logger
import uuid

corr_id = str(uuid.uuid4())
router = APIRouter()

# Initialize LLM and Portfolio
llm = Chain()
portfolio = Portfolio()
portfolio.load_portfolio()

# Request schema
class EmailRequest(BaseModel):
    input_type: str  # "Job URL" or "Job Description"
    input_value: str
    max_emails: int


@router.post("/generate-email")
def generate_email(request: EmailRequest):
    try:
        if request.input_type == "Job URL":
            loader = WebBaseLoader([request.input_value])
            page_content = loader.load().pop().page_content
            data = clean_text(page_content)
        else:
            data = clean_text(request.input_value)
        
        jobs = llm.extract_jobs(data)
        if not jobs:
            logger.warning(f"error: No jobs found in the provided input.", extra={"correlation_id": corr_id})
            return {"warning": "No jobs found in the provided input."}

        emails = []
        for _ in range(request.max_emails):
            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                emails.append({
                    "job_title": job.get("title", "Unknown Title"),
                    "job_description": job.get("description", ""),
                    "email": email
                })
                break  # only first job for now

        return {"emails": emails}
    
    except Exception as e:
        logger.error(f"error: {str(e)}", extra={"correlation_id": corr_id})
        return {"error": str(e)}
