import logging
from src.database.db_config import db
from src.database.models import Book

def add_sent_book(abs_book_data):
    """Registra un libro enviado en la DB."""
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
        db.session.add(book)
        db.session.commit()
        return book
    except Exception as e:
        logging.error(f"Error al agregar el libro a la base de datos: {e}", exc_info=True)
        db.session.rollback()
        return None

def was_book_sent(abs_id):
    """Verifica si un libro ya fue enviado."""
    try:
        query = db.session.query(Book.query.filter_by(abs_id=abs_id).exists()).scalar()
        return query
    except Exception as e:
        logging.error(f"Error al verificar si el libro fue enviado: {e}", exc_info=True)
        return False