# Build stage
FROM python:3.13-slim-bookworm as builder

WORKDIR /app

# Instala dependencias del sistema primero
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copia solo lo necesario
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip check

COPY src/ ./src/
COPY main.py .

# Usa usuario no-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "main.py"]