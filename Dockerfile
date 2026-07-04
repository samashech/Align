FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers and dependencies
RUN playwright install --with-deps chromium

# Download Spacy models
RUN python -m spacy download en_core_web_lg
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Hugging Face Spaces require running on port 7860
ENV PORT=7860
EXPOSE 7860

# Fix permissions for Hugging Face Spaces (so it can create SQLite db and uploads folder)
RUN chmod -R 777 /app

# Run the Flask app using Gunicorn
CMD ["gunicorn", "--worker-class", "gthread", "--threads", "4", "-b", "0.0.0.0:7860", "app:app"]
