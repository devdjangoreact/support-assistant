# Use an official lightweight Python image
FROM python:3.10-slim

RUN pip install poetry==1.6

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory in the container
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Copy the requirements file into the container
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy the content of the local src directory to the working directory
COPY . /app

# Specify the command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]