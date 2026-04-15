FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.5 && \
    poetry config virtualenvs.create false

# Copy common dependency first
COPY common/templates/backend /common/templates/backend

# Copy shell backend
COPY apps/shell/backend/pyproject.toml apps/shell/backend/poetry.lock* ./
RUN poetry install --no-dev --no-interaction --no-ansi --no-root

COPY apps/shell/backend/src/ ./src/
RUN poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "shell_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
