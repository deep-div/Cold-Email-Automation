import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from app.logs.logger import logger

load_dotenv()

class Chain:
    def __init__(self):
        groq_key = os.getenv("GROQ_API_KEY")
        logger.debug(f"GROQ_API_KEY Loaded: {bool(groq_key)}")

        self.llm = ChatGroq(
            temperature=0.3,
            groq_api_key=groq_key,
            model_name="llama-3.3-70b-versatile"
        )
        logger.info("ChatGroq LLM initialized successfully.")

    def extract_jobs(self, cleaned_text):
        logger.info(f"Received cleaned_text length: {len(cleaned_text)}")
        logger.debug(f"Cleaned_text content: {cleaned_text[:5000]}")  # Logs first 5000 chars

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm

        try:
            logger.info("Invoking LLM for job extraction...")
            res = chain_extract.invoke({"page_data": cleaned_text})
            logger.debug(f"Raw LLM Response: {res}")

            response_content = res.content
            logger.info("Parsing JSON response...")

            json_parser = JsonOutputParser()
            parsed = json_parser.parse(response_content)

            logger.debug(f"Parsed JSON: {parsed}")
            return parsed if isinstance(parsed, list) else [parsed]

        except Exception as e:
            logger.error(f"Failed job extraction: {str(e)}")
            raise OutputParserException("Context too big. Unable to parse jobs.")

    def write_mail(self, job, links):
        logger.info("Constructing cold email...")
        logger.debug(f"Job Provided: {job}")
        logger.debug(f"Portfolio Links Provided: {links}")

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Mohan, a business development executive at TCS. TCS is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of TCS 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase TCS's portfolio: {link_list}
            Remember you are Mohan, BDE at TCS. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm

        try:
            res = chain_email.invoke({
                "job_description": str(job),
                "link_list": links
            })

            logger.info("Email successfully generated.")
            logger.debug(f"Generated Email Content: {res.content}")
            return res.content

        except Exception as e:
            logger.error(f"Failed generating cold email: {str(e)}")
            raise RuntimeError("LLM failed to generate cold email.")
