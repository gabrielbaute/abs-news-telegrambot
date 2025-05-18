# Usa imagen con parches de seguridad
FROM python:3.12.0-slim-bookworm@sha256:8d10c926a382c8b7c87b6ff4b5d6e60a24a1b8c7b9e1a3e0e3a3e8e8b8e8b8e8

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