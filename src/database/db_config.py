from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from src.config import Config

db = SQLAlchemy()
Session = scoped_session(sessionmaker())

def init_db(app=None):
    """Initialize the database"""
    if app:
        # Flask mode with migrations
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        Migrate(app, db)
        with app.app_context():
            db.create_all()
    
    else:
        # Standalone mode without migrations (for scheduler)
        engine = create_engine(
            Config.SQLALCHEMY_DATABASE_URI,
            poolclass=NullPool,
            connect_args={'check_same_thread': False}
        )
        Session.configure(bind=engine)
        db.metadata.create_all(engine)