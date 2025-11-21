FROM python:3.11-slim-bullseye AS builder

# Metadata labels
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="Production-ready Dockerfile for FastAPI application"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim-bullseye

# Metadata labels
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="Production-ready Dockerfile for FastAPI application"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_USER=fastapi_user \
    APP_HOME=/app

# Create a non-root user
RUN groupadd -r $APP_USER && useradd --no-log-init -r -g $APP_USER $APP_USER

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR $APP_HOME

# Copy application code and dependencies from builder
COPY --from=builder /app /app

# Change ownership of the application directory
RUN chown -R $APP_USER:$APP_USER $APP_HOME

# Switch to non-root user
USER $APP_USER

# Expose the application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Explanation of the Dockerfile:
1. **Multi-Stage Builds**:
   - The `builder` stage installs dependencies to reduce the final image size.
   - The final stage (`FROM python:3.11-slim-bullseye`) only contains the application and runtime dependencies.

2. **Proper Caching**:
   - Dependencies are installed after copying `requirements.txt` to leverage Docker's build cache.

3. **Non-Root User**:
   - A non-root user (`fastapi_user`) is created and used to run the application for security.

4. **Health Checks**:
   - A health check is added to ensure the application is running and responding.

5. **Layer Ordering**:
   - Layers are ordered to maximize caching and minimize rebuilds.

6. **Specific Version Tags**:
   - The `python:3.11-slim-bullseye` image is used instead of `latest` for reproducibility.

7. **Security Best Practices**:
   - Unnecessary files and cache are removed to reduce the attack surface.
   - The application runs as a non-root user.

8. **Metadata Labels**:
   - Labels provide useful metadata about the image.

### Additional Notes:
- Replace `main:app` in the `CMD` instruction with the actual module and app name of your FastAPI application.
- Ensure you have a `/health` endpoint in your FastAPI app for the health check to work. If not, modify the `HEALTHCHECK` instruction accordingly.
- Add any additional dependencies to `requirements.txt` as needed.