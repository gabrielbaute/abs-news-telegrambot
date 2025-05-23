import requests
from src.config import Config

class AudiobookshelfAPI:
    def __init__(self):
        self.server_url = Config.SERVER_URL
        self.api_key = Config.API_KEY
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _get_authors(self, metadata):
        authors = metadata.get("authors", [])
        # Caso 1: authors es un diccionario único
        if isinstance(authors, dict):
            author = authors.get("name", "Autor desconocido")
        # Caso 2: authors es una lista de diccionarios
        elif isinstance(authors, list) and authors:
            author = ", ".join([a.get("name", "Autor desconocido") for a in authors])
        else:
            author = "Autor desconocido"
        
        return author
    
    def _get_narrators(self, metadata):
        narrators = metadata.get("narrators", [])
        # Caso 1: narrators es una lista de strings
        if isinstance(narrators, list) and narrators and isinstance(narrators[0], str):
            narrator = ", ".join(narrators)
        # Caso 2: narrators es una lista de diccionarios
        elif isinstance(narrators, list) and narrators and isinstance(narrators[0], dict):
            narrator = ", ".join([n.get("name", "Narrador desconocido") for n in narrators])
        else:
            narrator = "Narrador desconocido"
        
        return narrator
    
    def _get_description(self, metadata):
        description = metadata.get("description")
        formatted_description = "Sin descripción disponible."
        if description:
            formatted_description = f"{description[:500]}..." if len(description) > 500 else description
        
        return formatted_description

    def get_libraries(self):
        """Obtiene la lista de bibliotecas disponibles."""
        url = f"{self.server_url}/api/libraries"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("libraries", [])
        return None

    def get_all_books(self, library_id, batch_size=500):
        """Obtiene TODOS los libros de una biblioteca (maneja paginación)."""
        all_books = []
        page = 0
        
        while True:
            url = f"{self.server_url}/api/libraries/{library_id}/items?limit={batch_size}&page={page}"
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                break
                
            books = response.json().get("results", [])
            if not books:
                break
                
            all_books.extend(books)
            page += 1
        
        return all_books

    def get_books(self, library_id, limit=500):
        """Obtiene libros de una biblioteca específica."""
        url = f"{self.server_url}/api/libraries/{library_id}/items?limit={limit}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("results", [])
        return None

    def get_book_details(self, book_id):
        """Obtiene metadatos detallados de un libro por su ID."""
        url = f"{self.server_url}/api/items/{book_id}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    
    def format_book_message(self, book_details):
        media = book_details.get("media", {})
        metadata = media.get("metadata", {})
        audio_files = media.get("audioFiles", [])
        
        # Extrae la duración total sumando todos los archivos de audio
        duration_seconds = sum(audio_file.get("duration", 0) for audio_file in audio_files)
        duration = f"{duration_seconds // 3600}h {(duration_seconds % 3600) // 60}m" if duration_seconds > 0 else "Duración no disponible"

        # Resto del código (título, autor, etc.) igual...
        title = metadata.get("title", "Título desconocido")
        author = self._get_authors(metadata)
        narrator = self._get_narrators(metadata)
        description = self._get_description(metadata)
        genres = ", ".join(metadata.get("genres", [])) or "No especificado"
        language = metadata.get("language", "Idioma desconocido")
        cover_url = f"{self.server_url}/api/items/{book_details['id']}/cover" if book_details.get('id') else None

        # Formatea el mensaje (ajusta los campos según necesites)
        message = (
            "🎧 *¡AUDIOLIBRO DEL DÍA!* 🎧\n\n"
            f"📚 *{title}*\n"
            f"-> ✍️ *Autor(es):* {author}\n"
            f"-> 🎙️ *Narrador(es):* {narrator}\n"
            f"-> ⏳ *Duración:* {duration}\n"
            f"-> 🌍 *Idioma:* {language}\n"
            f"-> 🏷️ *Géneros:* {genres}\n\n"
            f"📖 *Sinopsis:* {description[:500]}...\n\n"

            "No olvides unirte al servidor de Audiobookshelf para más audiolibros:\n"
            "https://audiobook.enlaesquinadelsaman.online\n\n"
        )
        
        return {
            "message": message,
            "cover_url": cover_url
        }