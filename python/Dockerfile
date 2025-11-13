FROM python:3.12.10-slim AS builder

RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry with proper PATH setup
ENV POETRY_HOME=/opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# Install dependencies without dev packages
RUN poetry install --no-root --only main

# --- Stage 2: Final Runtime Image ---
FROM python:3.12.10-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy all application files
COPY . .

# Add /app to PYTHONPATH so imports work correctly
ENV PYTHONPATH=/app

EXPOSE 8000

WORKDIR /app/python
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]