# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Tests of the JWT tokens and of the `get_current_user_id` dependency."""

from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient

from service.auth.security import ISSUER, create_token, decode_token, get_current_user_id
from tests.conftest import JWT_SECRET


@pytest.fixture
def protected_client() -> TestClient:
    """Minimal application with a route protected by `get_current_user_id`."""
    app = FastAPI()

    @app.get("/me")
    async def read_me(user_id: Annotated[int, Depends(get_current_user_id)]) -> dict[str, int]:
        return {"id": user_id}

    return TestClient(app)


def forge_token(key: str = JWT_SECRET, **overrides: object) -> str:
    """Signed token (with the test key by default) whose claims can be changed, or removed with None."""
    now = datetime.now(UTC)
    claims: dict[str, object] = {"sub": "1", "iss": ISSUER, "iat": now, "exp": now + timedelta(minutes=5)}
    claims.update(overrides)
    kept_claims = {name: value for name, value in claims.items() if value is not None}
    return jwt.encode(kept_claims, key, algorithm="HS256")


def test_create_then_decode_token_returns_the_user_id() -> None:
    """A token created by the API decodes to the integer user id."""
    assert decode_token(create_token(sub="42")) == 42


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(forge_token(exp=datetime.now(UTC) - timedelta(seconds=1)), id="expired"),
        pytest.param(forge_token(iss="other-application"), id="other-issuer"),
        pytest.param(forge_token(sub="jdoe"), id="non-numeric-sub"),
        pytest.param(forge_token(sub=None), id="no-sub"),
        pytest.param(forge_token(exp=None), id="no-exp"),
        pytest.param(forge_token(iss=None), id="no-iss"),
        pytest.param(forge_token(key="other-key-0123456789abcdef0123456789"), id="wrong-signature"),
        pytest.param("not-a-jwt", id="malformed"),
    ],
)
def test_decode_token_rejects_invalid_tokens(token: str) -> None:
    """Any invalid token raises a 401 error."""
    with pytest.raises(HTTPException) as exc_info:
        decode_token(token)

    assert exc_info.value.status_code == 401


def test_protected_route_receives_the_user_id(protected_client: TestClient) -> None:
    """With a valid token, the route receives the user id."""
    response = protected_client.get("/me", headers={"Authorization": f"Bearer {create_token(sub='7')}"})

    assert response.status_code == 200
    assert response.json() == {"id": 7}


def test_protected_route_without_token_returns_401(protected_client: TestClient) -> None:
    """Without an Authorization header, access is denied."""
    response = protected_client.get("/me")

    assert response.status_code == 401


def test_protected_route_with_another_scheme_returns_401(protected_client: TestClient) -> None:
    """A scheme other than Bearer is rejected."""
    response = protected_client.get("/me", headers={"Authorization": f"Basic {create_token(sub='7')}"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(forge_token(exp=datetime.now(UTC) - timedelta(seconds=1)), id="expired"),
        pytest.param(forge_token(iss="other-application"), id="other-issuer"),
        pytest.param(forge_token(sub="jdoe"), id="non-numeric-sub"),
    ],
)
def test_protected_route_with_invalid_token_returns_401(protected_client: TestClient, token: str) -> None:
    """An invalid token is rejected with the same code as a missing one."""
    response = protected_client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
