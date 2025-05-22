# Use the official Python image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ./app ./app

# Expose FastAPI port
EXPOSE 8000

ARG ENV=dev  # Default to dev
ENV ENV=${ENV}

CMD ["/bin/sh", "-c", "if [ \"$ENV\" = \"prod\" ]; then gunicorn -w 4 --preload -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000; else uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; fi"]
