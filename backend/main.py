from fastapi import FastAPI
from backend.routes import router

app = FastAPI(
    title="📧 Cold Email Generator",
    description="Generate emails from Job URLs or Job Descriptions",
    version="1.0.0"
)

# Include router
app.include_router(router)


# uvicorn backend.main:app --reload --port 8000 
