FROM python:3.9-slim

WORKDIR /app

COPY frontend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY frontend ./frontend

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
