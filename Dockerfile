FROM python:3.13-rc-slim-bookworm

# Configuración de entorno seguro
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 1. Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Crea usuario y directorio de logs ANTES de cambiar de usuario
RUN groupadd -r appuser -g 1000 && \
    useradd -r -u 1000 -g appuser appuser && \
    mkdir -p /app/logs && \
    chown appuser:appuser /app/logs && \
    chmod 755 /app/logs

# 3. Instala dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# 4. Copia el código
COPY src/ ./src/
COPY main.py .

# 5. Cambia al usuario no-root
USER appuser

CMD ["python", "main.py"]