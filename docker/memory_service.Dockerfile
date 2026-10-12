FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first, so this layer is cached until pyproject.toml changes.
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# The app runs from /app, which is on sys.path for both uvicorn and alembic.
COPY alembic.ini ./
COPY memory_service ./memory_service
COPY ingest ./ingest
COPY hermes_plugin ./hermes_plugin
COPY jobs ./jobs
COPY migrations ./migrations

RUN useradd --create-home --uid 10001 app
USER app

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]

CMD ["uvicorn", "memory_service.api:app", "--host", "0.0.0.0", "--port", "8000"]
