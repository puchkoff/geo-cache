FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml README.md ./

# Copy application code
COPY geo_cache ./geo_cache

# Install dependencies and generate lock file
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && poetry lock

# Expose ports
EXPOSE 5000 80

# Run the application
CMD ["poetry", "run", "python", "-m", "geo_cache.app"]
