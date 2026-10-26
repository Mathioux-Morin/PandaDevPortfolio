# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Tests de la route POST /auth/token."""

import jwt
import pytest
lazy from fastapi.testclient import TestClient
lazy from sqlmodel import Session

from service.auth.security import ISSUER
from service.db.models import Utilisateur
from tests.conftest import JWT_SECRET, PASSWORD, pgcrypto_hash


def test_bons_identifiants_renvoient_un_token_bearer(client: TestClient, user: Utilisateur) -> None:
    """Un login et un mot de passe corrects donnent un token."""
    response = client.post("/auth/token", json={"login": user.login, "password": PASSWORD})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_le_token_ne_contient_que_l_identifiant(client: TestClient, user: Utilisateur) -> None:
    """Le token porte uniquement sub, iss, iat et exp, avec une validité de 30 minutes."""
    response = client.post("/auth/token", json={"login": user.login, "password": PASSWORD})

    payload = jwt.decode(response.json()["access_token"], JWT_SECRET, algorithms=["HS256"], issuer=ISSUER)
    assert set(payload) == {"sub", "iss", "iat", "exp"}
    assert payload["sub"] == str(user.id)
    assert payload["exp"] - payload["iat"] == 30 * 60


@pytest.mark.parametrize(
    ("login", "password"),
    [
        pytest.param("jdoe", "mauvais mot de passe", id="mauvais-mot-de-passe"),
        pytest.param("inconnu", PASSWORD, id="login-inconnu"),
        pytest.param("JDOE", PASSWORD, id="login-sensible-a-la-casse"),
        pytest.param("jdoe", "", id="mot-de-passe-vide"),
    ],
)
@pytest.mark.usefixtures("user")
def test_identifiants_invalides_renvoient_401(client: TestClient, login: str, password: str) -> None:
    """Toute erreur d'identifiants donne 401."""
    response = client.post("/auth/token", json={"login": login, "password": password})

    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.usefixtures("user")
def test_login_inconnu_et_mauvais_mot_de_passe_sont_indiscernables(client: TestClient) -> None:
    """La réponse ne révèle pas si le login existe."""
    unknown_login = client.post("/auth/token", json={"login": "inconnu", "password": PASSWORD})
    wrong_password = client.post("/auth/token", json={"login": "jdoe", "password": "faux"})

    assert unknown_login.json() == wrong_password.json()


def test_mot_de_passe_de_plus_de_72_octets_tronque_comme_pgcrypto(client: TestClient, session: Session) -> None:
    """Comme pgcrypto, seuls les 72 premiers octets comptent, sans erreur pour un mot de passe plus long."""
    long_password = "é" * 50  # 100 octets en UTF-8
    session.add(Utilisateur(login="long", mot_de_passe=pgcrypto_hash(long_password)))
    session.commit()

    full = client.post("/auth/token", json={"login": "long", "password": long_password})
    same_first_72_bytes = client.post("/auth/token", json={"login": "long", "password": "é" * 36 + "suite"})

    assert full.status_code == 200
    assert same_first_72_bytes.status_code == 200


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"id": "jdoe", "displayname": "John Doe", "authorization": "admin"}, id="ancien-format"),
        pytest.param({"login": "jdoe"}, id="mot-de-passe-manquant"),
        pytest.param({"password": PASSWORD}, id="login-manquant"),
        pytest.param({"login": "jdoe", "password": PASSWORD, "authorization": "admin"}, id="champ-en-trop"),
    ],
)
@pytest.mark.usefixtures("user")
def test_corps_invalide_renvoie_422(client: TestClient, body: dict[str, str]) -> None:
    """Un corps incomplet ou avec des champs inconnus est refusé."""
    response = client.post("/auth/token", json=body)

    assert response.status_code == 422


@pytest.mark.usefixtures("user")
def test_le_mot_de_passe_n_apparait_pas_dans_l_erreur_de_validation(client: TestClient) -> None:
    """Le mot de passe (SecretStr) n'est jamais renvoyé dans les erreurs 422."""
    response = client.post("/auth/token", json={"login": "jdoe", "password": PASSWORD, "extra": "x"})

    assert PASSWORD not in response.text
