import logging
import sys
from io import TextIOWrapper
from pathlib import Path
from datetime import datetime

def setup_logging():
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / f"bot_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # Configuración mejorada con encoding UTF-8
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(stream=sys.stdout)
        ]
    )
    
    # Configuración adicional para la consola en Windows
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    return logging.getLogger("AudiobookshelfBot")