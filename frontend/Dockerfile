FROM python:3.9-slim

WORKDIR /app

COPY frontend ./frontend

RUN pip install --no-cache-dir -r ./frontend/requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
