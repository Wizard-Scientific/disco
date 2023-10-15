import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..utils.config import init_config

engine = create_engine(os.getenv("DB_URI_DISCO"),
    echo=False
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

from .channel_metrics import ChannelMetrics
from .guild import Guild
