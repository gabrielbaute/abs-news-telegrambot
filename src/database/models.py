from src.database.db_config import db
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4

class User(db.Model, UserMixin):
    """User model for the database."""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True,  default=lambda: str(uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(36), default=str(uuid4()), unique=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    __tablename__ = 'sent_books'  # Nombre más descriptivo
    
    id = db.Column(db.Integer, primary_key=True)
    abs_id = db.Column(db.String(36), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100))  # Nuevo campo útil
    genres = db.Column(db.String(200))  # Cadena separada por comas
    duration = db.Column(db.Integer)  # Duración en segundos
    language = db.Column(db.String(50))
    cover_url = db.Column(db.String(255))  # Para posible reutilización
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de envío
    
    # Relación opcional con usuarios (si quieres trackear quién lo envió)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    user = db.relationship('User', backref='sent_books')

    def __repr__(self):
        return f'<Book {self.title} (ABS: {self.abs_id})>'
