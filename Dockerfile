FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create cache and data directories with proper permissions
RUN mkdir -p /.cache && chmod 777 /.cache
RUN mkdir -p /tmp/chrome_langchain_db && chmod 777 /tmp/chrome_langchain_db

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the embedding model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L3-v2')"

# Copy the rest of the application
COPY . .

# Make port 7860 available (Hugging Face uses this port)
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
