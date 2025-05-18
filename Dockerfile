# Usa la última imagen estable de Python 3.12 (o 3.13 si prefieres)
FROM python:3.13-rc-slim-bookworm 

# Configuración de entorno seguro
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1. Instala dependencias del sistema solo las esenciales
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Copia e instala dependencias Python primero (para cache eficiente)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# 3. Copia el resto del código
COPY src/ ./src/
COPY main.py .

# 4. Crea usuario no-root
RUN useradd -r -s /bin/false appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["python", "main.py"]