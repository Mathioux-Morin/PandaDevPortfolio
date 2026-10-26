# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Tests des tokens JWT et de la dépendance `get_current_user_id`."""

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
    """Application minimale avec une route protégée par `get_current_user_id`."""
    app = FastAPI()

    @app.get("/moi")
    async def read_me(user_id: Annotated[int, Depends(get_current_user_id)]) -> dict[str, int]:
        return {"id": user_id}

    return TestClient(app)


def forge_token(key: str = JWT_SECRET, **overrides: object) -> str:
    """Token signé (par défaut avec la clé de test), dont on peut modifier ou retirer (valeur None) des claims."""
    now = datetime.now(UTC)
    claims: dict[str, object] = {"sub": "1", "iss": ISSUER, "iat": now, "exp": now + timedelta(minutes=5)}
    claims.update(overrides)
    return jwt.encode({k: v for k, v in claims.items() if v is not None}, key, algorithm="HS256")


def test_create_token_puis_decode_token_renvoie_l_identifiant() -> None:
    """Un token créé par l'API se décode en l'identifiant entier de la personne."""
    assert decode_token(create_token(sub="42")) == 42


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(forge_token(exp=datetime.now(UTC) - timedelta(seconds=1)), id="expire"),
        pytest.param(forge_token(iss="autre-application"), id="autre-emetteur"),
        pytest.param(forge_token(sub="jdoe"), id="sub-non-numerique"),
        pytest.param(forge_token(sub=None), id="sans-sub"),
        pytest.param(forge_token(exp=None), id="sans-exp"),
        pytest.param(forge_token(iss=None), id="sans-iss"),
        pytest.param(forge_token(key="autre-cle-0123456789abcdef0123456789"), id="mauvaise-signature"),
        pytest.param("pas-un-jwt", id="malforme"),
    ],
)
def test_decode_token_refuse_les_tokens_invalides(token: str) -> None:
    """Tout token invalide lève une erreur 401."""
    with pytest.raises(HTTPException) as exc_info:
        decode_token(token)

    assert exc_info.value.status_code == 401


def test_route_protegee_recoit_l_identifiant(protected_client: TestClient) -> None:
    """Avec un token valide, la route reçoit l'identifiant de la personne."""
    response = protected_client.get("/moi", headers={"Authorization": f"Bearer {create_token(sub='7')}"})

    assert response.status_code == 200
    assert response.json() == {"id": 7}


def test_route_protegee_sans_token_renvoie_401(protected_client: TestClient) -> None:
    """Sans en-tête Authorization, l'accès est refusé."""
    response = protected_client.get("/moi")

    assert response.status_code == 401


def test_route_protegee_avec_un_autre_schema_renvoie_401(protected_client: TestClient) -> None:
    """Un schéma autre que Bearer est refusé."""
    response = protected_client.get("/moi", headers={"Authorization": f"Basic {create_token(sub='7')}"})

    assert response.status_code == 401


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(forge_token(exp=datetime.now(UTC) - timedelta(seconds=1)), id="expire"),
        pytest.param(forge_token(iss="autre-application"), id="autre-emetteur"),
        pytest.param(forge_token(sub="jdoe"), id="sub-non-numerique"),
    ],
)
def test_route_protegee_avec_un_token_invalide_renvoie_401(protected_client: TestClient, token: str) -> None:
    """Un token invalide est refusé avec le même code qu'un token absent."""
    response = protected_client.get("/moi", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
