import logging
from sqlmodel import SQLModel, Session, create_engine
from app.config import get_settings
from contextlib import contextmanager

logger = logging.getLogger(__name__)

_db_uri = get_settings().database_uri
_is_sqlite = _db_uri.startswith("sqlite")

if _is_sqlite:
    engine = create_engine(
        _db_uri,
        echo=get_settings().env.lower() in ["dev", "development"],
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(
        _db_uri,
        echo=get_settings().env.lower() in ["dev", "development"],
        pool_size=10,
        max_overflow=10,
        pool_timeout=10,
        pool_recycle=300,
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_all():
    SQLModel.metadata.drop_all(bind=engine)


def _session_generator():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()


def get_session():
    yield from _session_generator()


def get_db():
    yield from _session_generator()


@contextmanager
def get_cli_session():
    yield from _session_generator()
