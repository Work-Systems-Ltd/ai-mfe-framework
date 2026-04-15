FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.5 && \
    poetry config virtualenvs.create false

COPY common/templates/backend /common/templates/backend
COPY apps/permissions/backend/pyproject.toml apps/permissions/backend/poetry.lock* ./
RUN poetry install --no-dev --no-interaction --no-ansi --no-root

COPY apps/permissions/backend/src/ ./src/
RUN poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "permissions_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
