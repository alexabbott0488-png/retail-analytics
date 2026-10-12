FROM python:3.11-slim

# System dependencies for OpenCV, audio, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Non-root user
RUN useradd -m -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY configs/ ./configs/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080 8000 8001

CMD ["python", "-m", "app.main"]