import logging
from src.database.db_config import session_scope
from src.database.models import Book

logger = logging.getLogger("AudiobookshelfBot.database")

def add_sent_book(abs_book_data):
    """
    Registra un libro enviado en la DB.
    
    Args:
        abs_book_data (dict): Datos del libro desde la API de Audiobookshelf
    
    Returns:
        Book | None: Instancia del libro guardado o None si falla
    """
    book = Book(
        abs_id=abs_book_data["id"],
        title=abs_book_data["media"]["metadata"]["title"],
        author=", ".join(a["name"] for a in abs_book_data["media"]["metadata"].get("authors", [])),
        narrator=", ".join(abs_book_data["media"]["metadata"].get("narrators", [])),
        genres=", ".join(abs_book_data["media"]["metadata"].get("genres", [])),
        duration=sum(f["duration"] for f in abs_book_data["media"]["audioFiles"]),
        cover_url=f"/api/items/{abs_book_data['id']}/cover" if abs_book_data.get("id") else None
    )
    
    try:
        with session_scope() as session:
            session.add(book)
            # No necesitamos commit explícito (lo hace session_scope)
            logger.info(f"Libro añadido a DB: {book.abs_id} - {book.title}")
            return book
    except Exception as e:
        logger.error(f"Error al agregar libro {abs_book_data.get('id')}: {e}", exc_info=True)
        return None

def was_book_sent(abs_id):
    """
    Verifica si un libro ya fue enviado.
    
    Args:
        abs_id (str): ID del libro en Audiobookshelf
    
    Returns:
        bool: True si existe, False si no existe o hay error
    """
    try:
        with session_scope() as session:
            exists = session.query(
                session.query(Book).filter_by(abs_id=abs_id).exists()
            ).scalar()
            logger.debug(f"Verificación de libro {abs_id}: {'Existe' if exists else 'No existe'}")
            return exists
    except Exception as e:
        logger.error(f"Error al verificar libro {abs_id}: {e}", exc_info=True)
        return False  # Asumimos que no fue enviado si hay error