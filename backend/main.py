from fastapi import FastAPI
from backend.routes import router
from backend.metrics import setup_metrics   # import metrics

app = FastAPI(
    title="📧 Cold Email Generator",
    description="Generate emails from Job URLs or Job Descriptions",
    version="1.0.0"
)

# MUST be called before the app starts serving
setup_metrics(app)

# Include router
app.include_router(router)



# uvicorn backend.main:app --reload --port 8000
