# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Shared fixtures: test JWT settings and in-memory SQLite database."""

lazy from collections.abc import Iterator

import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
lazy from sqlalchemy import Engine

from my_api import app
from service.db.database import get_session
from service.db.models import User

JWT_SECRET = "test-only-secret-key-0123456789abcdef0123456789"
PASSWORD = "secret password"


def pgcrypto_hash(password: str) -> str:
    """Bcrypt hash in the format produced by pgcrypto: crypt(..., gen_salt('bf')).

    pgcrypto truncates to 72 bytes and uses the `$2a$` prefix. Low cost for fast tests.
    """
    password_hash = bcrypt.hashpw(password.encode()[:72], bcrypt.gensalt(rounds=4)).decode()
    return password_hash.replace("$2b$", "$2a$", 1)


@pytest.fixture(autouse=True)
def jwt_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test JWT settings, read by `get_jwt_settings` on each call."""
    monkeypatch.setenv("JWT_SECRET_KEY", JWT_SECRET)
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")


@pytest.fixture
def engine() -> Iterator[Engine]:
    """In-memory SQLite database, shared between threads (TestClient) thanks to StaticPool."""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Session on the test database."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def user(session: Session) -> User:
    """User `jdoe` whose password is `PASSWORD`."""
    user = User(login="jdoe", password_hash=pgcrypto_hash(PASSWORD))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def client(engine: Engine) -> Iterator[TestClient]:
    """HTTP client of the application, plugged into the test database."""

    def override_get_session() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
