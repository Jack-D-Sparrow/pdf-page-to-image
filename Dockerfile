FROM python:3.10-slim

# Install poppler for pdf2image
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 10000

# Run the app
CMD ["python", "app.py"]
