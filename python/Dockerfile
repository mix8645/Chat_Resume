# --- Stage 1: Builder ---
FROM python:3.12.10-slim AS builder

# Install SSL dependencies and curl
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION="1.8.3" \
    PATH="$POETRY_HOME/bin:$PATH"

# Install poetry AND configure it in a single RUN command using '&&'
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && (export PATH="$POETRY_HOME/bin:$PATH" && poetry config virtualenvs.create false)


WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# Install dependencies, ensuring pymongo[tls] is available if you use it in pyproject.toml
RUN poetry install --no-root --no-dev

# --- Stage 2: Final Runtime Image ---
FROM python:3.12.10-slim

# Install the same SSL dependencies in the final runtime stage
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder to the final image's site-packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy your application code
COPY . .

CMD ["python", "app.py"]