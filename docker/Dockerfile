# Use official Python 3.11 image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /Cold-Email-Automation

# Copy requirements first for caching
COPY requirements.txt ./requirements.txt
COPY .env ./.env

# Copy the app and tests folder into container
COPY app ./app
COPY tests ./tests

# Install dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Set PYTHONPATH for imports
ENV PYTHONPATH=/Cold-Email-Automation

# Expose container port (optional, for documentation)
EXPOSE 8501

# Start Streamlit app on port 8501
CMD ["python", "-m", "streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
