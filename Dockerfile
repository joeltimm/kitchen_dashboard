# kitchen_dashboard/Dockerfile

FROM python:3.12-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask port
EXPOSE 5050

RUN useradd -m appuser
USER appuser


# Start app with Gunicorn
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:5050", "--timeout=30", "--worker-class=sync", "backend.app:app"]
