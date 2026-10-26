# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Moteur PostgreSQL et gestion des sessions."""

from functools import cache
lazy from collections.abc import Iterator

from sqlalchemy import Engine, make_url
from sqlmodel import Session, create_engine

from service.settings.database import get_database_settings


@cache
def get_engine() -> Engine:
    """Crée le moteur SQLAlchemy une seule fois pour partager le pool de connexions.

    `DATABASE_URL` reste au format `postgresql://` (utilisable tel quel par psql) :
    le driver psycopg 3 est imposé ici.

    Returns:
        Engine: Le moteur connecté à la base.
    """
    url = make_url(str(get_database_settings().url)).set(drivername="postgresql+psycopg")
    return create_engine(url, pool_pre_ping=True)


def get_session() -> Iterator[Session]:
    """Fournit une session de base de données, fermée à la fin de la requête.

    Yields:
        Session: La session SQLModel.
    """
    with Session(get_engine()) as session:
        yield session
