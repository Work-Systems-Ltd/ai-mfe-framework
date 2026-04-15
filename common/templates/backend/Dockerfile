FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.5 && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-interaction --no-ansi

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "mfe_common.app_factory:create_app", "--host", "0.0.0.0", "--port", "8000"]
