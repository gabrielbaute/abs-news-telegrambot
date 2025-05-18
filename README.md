# 📚 Audiobookshelf Telegram Bot

![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

Un bot de Telegram que recomienda audiolibros diarios desde tu servidor Audiobookshelf. Perfecto para comunidades literarias.

## 🌟 Características

- ✅ Publicación automática diaria de audiolibros
- ✅ Portada, metadatos y reseña en cada publicación
- ✅ Selección aleatoria de tu biblioteca
- ✅ Configuración flexible por variables de entorno
- ✅ Registro detallado de actividades (logs)
- ✅ Optimizado para Docker y entornos cloud

## 🚀 Instalación Rápida

### Requisitos previos
- Docker Engine 20.10+
- Docker Compose 2.5+
- Servidor Audiobookshelf accesible

```bash
git clone https://github.com/gabrielbaute/abs-news-telegrambot
cd abs-news-telegrambot
```

## 🔧 Configuración

1. Copia el archivo de ejemplo y edítalo:
```bash
cp example.env .env
nano .env
```

2. Configura estas variables esenciales:
```ini
# Audiobookshelf
SERVER_URL=http://tuservidor:13378
API_KEY=tu_api_key_audiobookshelf

# Telegram
TELEGRAM_BOT_TOKEN=token_del_bot
TELEGRAM_CHAT_ID=id_del_grupo

# Programación
SCHEDULER_TIME_HOUR=9
SCHEDULER_TIME_MINUTE=0
TZ=America/Caracas
```

## 🐳 Despliegue con Docker

```bash
# Construir la imagen
docker-compose build

# Iniciar el servicio
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🛠️ Estructura del Proyecto

```
audiobookshelf-bot/
├── docker-compose.yml
├── Dockerfile
├── .env
├── requirements.txt
├── main.py
└── src/
    ├── bot/          # Lógica del bot de Telegram
    ├── config/       # Configuración y logging
    └── core/         # Conexión con Audiobookshelf
```

## ⚙️ Personalización Avanzada

### Cambiar frecuencia de publicación
Edita el trigger en `src/bot/scheduler.py`:
```python
# Ejemplo para enviar a las 9 AM y 5 PM
trigger = CronTrigger(hour='9,17', minute=0)
```

### Variables de entorno opcionales
| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `LOG_LEVEL` | Nivel de detalle de logs | `INFO` |
| `COVER_ASPECT_RATIO` | Proporción de portadas | `1` |

## 📈 Monitorización

Los logs se guardan en:
- Archivo: `./logs/bot_YYYY-MM-DD.log`
- Docker: `docker-compose logs -f`

Ejemplo de entrada de log:
```
2025-05-18 09:00:03 - INFO - Libro enviado: "El Principito" (ID: af4d3727...)
```

## 🤝 Contribución

1. Haz fork del proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -am 'Añade x funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## ⚠️ Solución de Problemas

**Error:** `'NoneType' object is not subscriptable`
- Solución: Verifica que todos los libros tengan metadatos completos en Audiobookshelf

**Error:** Problemas de conexión con la API
- Verifica:
  - `SERVER_URL` accesible desde el contenedor
  - `API_KEY` con permisos suficientes

## 📄 Licencia

MIT License - Copyright (c) 2025 [Gabriel Bauute]

---

💡 **Tip**: Para una instalación en producción, considera usar:
- Secrets de Docker para variables sensibles
- Sistema de monitorización como Prometheus+Grafana
- Backup regular del volumen de logs

¿Preguntas? ¡Abre un issue o contáctame directamente!