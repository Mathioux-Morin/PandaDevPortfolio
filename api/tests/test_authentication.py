# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Tests of the POST /auth/token route."""

import jwt
import pytest
lazy from fastapi.testclient import TestClient
lazy from sqlmodel import Session

from service.auth.security import ISSUER
from service.db.models import User
from tests.conftest import JWT_SECRET, PASSWORD, pgcrypto_hash


def test_valid_credentials_return_a_bearer_token(client: TestClient, user: User) -> None:
    """A correct login and password give a token."""
    response = client.post("/auth/token", json={"login": user.login, "password": PASSWORD})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_token_only_contains_the_user_id(client: TestClient, user: User) -> None:
    """The token only carries sub, iss, iat and exp, valid for 30 minutes."""
    response = client.post("/auth/token", json={"login": user.login, "password": PASSWORD})

    payload = jwt.decode(response.json()["access_token"], JWT_SECRET, algorithms=["HS256"], issuer=ISSUER)
    assert set(payload) == {"sub", "iss", "iat", "exp"}
    assert payload["sub"] == str(user.id)
    assert payload["exp"] - payload["iat"] == 30 * 60


@pytest.mark.parametrize(
    ("login", "password"),
    [
        pytest.param("jdoe", "wrong password", id="wrong-password"),
        pytest.param("unknown", PASSWORD, id="unknown-login"),
        pytest.param("JDOE", PASSWORD, id="case-sensitive-login"),
        pytest.param("jdoe", "", id="empty-password"),
    ],
)
@pytest.mark.usefixtures("user")
def test_invalid_credentials_return_401(client: TestClient, login: str, password: str) -> None:
    """Any credential error gives 401."""
    response = client.post("/auth/token", json={"login": login, "password": password})

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.usefixtures("user")
def test_unknown_login_and_wrong_password_are_indistinguishable(client: TestClient) -> None:
    """The response does not reveal whether the login exists."""
    unknown_login = client.post("/auth/token", json={"login": "unknown", "password": PASSWORD})
    wrong_password = client.post("/auth/token", json={"login": "jdoe", "password": "wrong"})

    assert unknown_login.json() == wrong_password.json()


def test_password_longer_than_72_bytes_is_truncated_like_pgcrypto(client: TestClient, session: Session) -> None:
    """Like pgcrypto, only the first 72 bytes count, with no error for a longer password."""
    long_password = "é" * 50  # 100 bytes in UTF-8
    session.add(User(login="long", password_hash=pgcrypto_hash(long_password)))
    session.commit()

    full_password = client.post("/auth/token", json={"login": "long", "password": long_password})
    same_first_72_bytes = client.post("/auth/token", json={"login": "long", "password": "é" * 36 + "suffix"})

    assert full_password.status_code == 200
    assert same_first_72_bytes.status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"id": "jdoe", "displayname": "John Doe", "authorization": "admin"}, id="old-format"),
        pytest.param({"login": "jdoe"}, id="missing-password"),
        pytest.param({"password": PASSWORD}, id="missing-login"),
        pytest.param({"login": "jdoe", "password": PASSWORD, "authorization": "admin"}, id="extra-field"),
    ],
)
@pytest.mark.usefixtures("user")
def test_invalid_body_returns_422(client: TestClient, body: dict[str, str]) -> None:
    """An incomplete body or one with unknown fields is rejected."""
    response = client.post("/auth/token", json=body)

    assert response.status_code == 422


@pytest.mark.usefixtures("user")
def test_password_is_not_echoed_in_validation_errors(client: TestClient) -> None:
    """The password (SecretStr) is never returned in 422 errors."""
    response = client.post("/auth/token", json={"login": "jdoe", "password": PASSWORD, "extra": "x"})

    assert PASSWORD not in response.text
