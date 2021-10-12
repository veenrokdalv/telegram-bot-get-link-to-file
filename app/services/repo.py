from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker


class Repo:
    """Repository."""

    def __init__(self, db_session: sessionmaker, db_engine: AsyncEngine):
        self.db_session = db_session
        self.db_engine = db_engine
