# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Module de sécurité pour la gestion des tokens JWT et de l'authentification."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from service.db.models import Utilisateur
from service.settings.auth import get_jwt_settings

logger = logging.getLogger(__name__)

ISSUER = "pandadev-portfolio"

# bcrypt ne prend en compte que les 72 premiers octets du mot de passe. pgcrypto tronque
# silencieusement, alors que la librairie Python lève une erreur : on tronque pareil.
BCRYPT_MAX_BYTES = 72

# Hash vérifié quand le login n'existe pas, pour que le temps de réponse
# ne révèle pas si un compte existe.
_DUMMY_HASH = bcrypt.hashpw(b"", bcrypt.gensalt())


def authenticate_user(session: Session, login: str, password: str) -> Utilisateur | None:
    """Vérifie le login et le mot de passe d'une personne.

    Args:
        session (Session): La session de base de données.
        login (str): Le login saisi.
        password (str): Le mot de passe saisi, en clair.

    Returns:
        Utilisateur | None: La personne si les identifiants sont corrects, sinon None.
    """
    user = session.exec(select(Utilisateur).where(Utilisateur.login == login)).first()
    hashed = user.mot_de_passe.encode() if user else _DUMMY_HASH
    password_ok = bcrypt.checkpw(password.encode()[:BCRYPT_MAX_BYTES], hashed)
    return user if user and password_ok else None


def create_token(sub: str) -> str:
    """Crée un token JWT pour une personne.

    Args:
        sub (str): Identifiant de la personne (subject du token).

    Returns:
        str: Le token encodé
    """
    settings = get_jwt_settings()
    now = datetime.now(UTC)
    to_encode: dict[str, object] = {
        "sub": sub,
        "iss": ISSUER,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> int:
    """Décode un token JWT et retourne l'identifiant de la personne.

    Args:
        token (str): Le token JWT à décoder.

    Returns:
        int: L'identifiant de la personne (`sub`).

    Raises:
        HTTPException: Si le token est invalide, expiré, d'un autre émetteur ou sans `sub` valide.
    """
    settings = get_jwt_settings()
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            issuer=ISSUER,
            options={"require": ["exp", "iss", "sub"]},
        )
        return int(payload["sub"])
    except (InvalidTokenError, ValueError) as e:
        logger.info("Token JWT refusé : %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token invalide ou expiré.",
                "description": "Le token JWT fourni est invalide ou a expiré.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


# Refuse en 401 les requêtes sans en-tête `Authorization: Bearer <token>`.
bearer_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> int:
    """Récupère l'identifiant de la personne connectée à partir du token JWT.

    À utiliser comme dépendance des routes protégées.

    Args:
        credentials (HTTPAuthorizationCredentials): Les credentials extraits de la requête.

    Returns:
        int: L'identifiant de la personne connectée.

    Raises:
        HTTPException: 401 si le token est absent, invalide ou expiré.
    """
    return decode_token(credentials.credentials)
