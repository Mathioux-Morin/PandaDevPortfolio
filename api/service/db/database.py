# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""PostgreSQL engine and session management."""

from functools import cache
lazy from collections.abc import Iterator

from sqlalchemy import Engine, make_url
from sqlmodel import Session, create_engine

from service.settings.database import get_database_settings


@cache
def get_engine() -> Engine:
    """Create the SQLAlchemy engine once, so the connection pool is shared.

    `DATABASE_URL` stays in the `postgresql://` format (usable as is by psql):
    the psycopg 3 driver is forced here.

    Returns:
        Engine: The engine connected to the database.
    """
    url = make_url(str(get_database_settings().url)).set(drivername="postgresql+psycopg")
    return create_engine(url, pool_pre_ping=True)


def get_session() -> Iterator[Session]:
    """Provide a database session, closed at the end of the request.

    Yields:
        Session: The SQLModel session.
    """
    with Session(get_engine()) as session:
        yield session
