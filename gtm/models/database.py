from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gtm.models.base import Base
from gtm.models.leads import Lead

def get_database_engine(db_url="sqlite:///data/leads.db"):
    """
    Initializes the database engine and creates tables if they don't exist.

    Args:
        db_url (str): Database URL (default is SQLite).

    Returns:
        Engine: SQLAlchemy engine instance.
    """
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)  # Create tables if not already present
    return engine

def get_session(engine):
    """
    Returns a new database session.

    Args:
        engine (Engine): SQLAlchemy engine instance.

    Returns:
        Session: SQLAlchemy session.
    """
    Session = sessionmaker(bind=engine)
    return Session()

