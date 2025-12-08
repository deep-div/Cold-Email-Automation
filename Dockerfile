# Use official Python 3.11 image as base
FROM python:3.11

# Set working directory inside container
WORKDIR /Cold-Email-Automation

# Copy requirements first for caching
COPY requirements.txt /Cold-Email-Automation/requirements.txt
COPY .env /Cold-Email-Automation/.env

# Copy the app folder into container
COPY app /Cold-Email-Automation/app

# Install dependencies
RUN pip install --no-cache-dir -r /Cold-Email-Automation/requirements.txt

# Set PYTHONPATH for imports
ENV PYTHONPATH=/Cold-Email-Automation

# Expose container port (optional, for documentation)
EXPOSE 8501

# Start Streamlit app on port 8501
CMD ["streamlit", "run", "/Cold-Email-Automation/app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
