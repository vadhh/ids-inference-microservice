# Use Python 3.10-slim to match your training environment (conda requirements.txt)
FROM python:3.10-slim

# Set environment variables to prevent pyc files and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies
COPY requirements.prod.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.prod.txt

# Copy the Application Code
COPY ./app /code/app

# Copy the Trained Models
COPY ./models /code/models

# Expose API port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]