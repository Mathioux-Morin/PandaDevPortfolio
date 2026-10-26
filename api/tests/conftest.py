# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Fixtures communes : configuration JWT de test et base SQLite en mémoire."""

lazy from collections.abc import Iterator

import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
lazy from sqlalchemy import Engine

from my_api import app
from service.db.database import get_session
from service.db.models import Utilisateur

JWT_SECRET = "cle-de-test-uniquement-0123456789abcdef0123456789"
PASSWORD = "mot de passe"


def pgcrypto_hash(password: str) -> str:
    """Hash bcrypt au format produit par pgcrypto : crypt(..., gen_salt('bf')).

    pgcrypto tronque à 72 octets et produit le préfixe `$2a$`. Coût réduit pour des tests rapides.
    """
    hashed = bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt(rounds=4)).decode()
    return hashed.replace("$2b$", "$2a$", 1)


@pytest.fixture(autouse=True)
def jwt_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configuration JWT de test, lue par `get_jwt_settings` à chaque appel."""
    monkeypatch.setenv("JWT_SECRET_KEY", JWT_SECRET)
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")


@pytest.fixture
def engine() -> Iterator[Engine]:
    """Base SQLite en mémoire, partagée entre les threads (TestClient) grâce à StaticPool."""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Session sur la base de test."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def user(session: Session) -> Utilisateur:
    """Personne `jdoe` dont le mot de passe est `PASSWORD`."""
    user = Utilisateur(login="jdoe", mot_de_passe=pgcrypto_hash(PASSWORD))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def client(engine: Engine) -> Iterator[TestClient]:
    """Client HTTP de l'application, branché sur la base de test."""

    def override_get_session() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
