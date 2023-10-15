import os
import gzip
import logging

from .. import Base, engine, db_session

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError


all_tables = [
    'guild',
    'channel_metrics',
]


def drop_db():
    Base.metadata.drop_all(engine)
    with engine.connect() as c:
        try:
            c.execute(text("drop table alembic_version;"))
        except ProgrammingError:
            logging.warn("did not drop alembic_version")


def dump_table(table, destination):
    """
    Dump SQL table to CSV.

    Low-level Postgres COPY data directly to CSV from database.
    """
    with gzip.open(destination, 'wb') as f:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cmd = f"COPY {table} to STDOUT WITH CSV HEADER"
        cursor.copy_expert(cmd, f)


def dump_all(destination):
    """
    Iterate across all tables and dump them to CSV.
    """
    if not os.path.isdir(destination):
        os.mkdir(destination)

    for table in all_tables:
        logging.info(f"Export {table}")
        dump_table(table, f"{destination}/{table}.csv")


def load_table(table, source):
    """
    Load SQL table from CSV.

    Low-level Postgres COPY data directly from CSV to database.
    """
    with gzip.open(source, 'rb') as f:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cmd = f"COPY {table} FROM STDIN WITH CSV HEADER"
        cursor.copy_expert(cmd, f)
        conn.commit()


def load_all(source):
    """
    Iterate across all tabeles, load them from CSV, and reset counters.
    """

    for table in all_tables:
        csv_filename = f"{source}/{table}.csv"
        logging.info(f"Load {table} from {csv_filename}")
        try:
            load_table(table, csv_filename)
            update_sequences_psql = f"SELECT setval('{table}_id_seq', max(id)) FROM {table};"
            db_session.execute(update_sequences_psql)
        except FileNotFoundError:
            logging.error(f"Unable to load data from '{csv_filename}'")
