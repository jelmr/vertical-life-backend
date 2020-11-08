from tornado_sqlalchemy import SQLAlchemy

db = SQLAlchemy('sqlite:///app.db', engine_options={'echo': False})


def get_db() -> SQLAlchemy:
    return db
