# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update

# Install Python dependencies
COPY ./requirements.txt /app/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10-slim-buster as runner

WORKDIR /app

# Install system dependencies
RUN apt-get update

COPY --from=builder /app/wheels /app/wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /app/wheels/*
RUN pip install uvicorn

# Copy project
COPY . /app/streamer

# Define the command to start the container
CMD python -m streamer.stream