# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""JWT token management and authentication."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from service.db.models import User
from service.settings.auth import get_jwt_settings

logger = logging.getLogger(__name__)

ISSUER = "pandadev-portfolio"

# bcrypt only uses the first 72 bytes of the password. pgcrypto truncates silently,
# whereas the Python library raises an error: truncate the same way.
BCRYPT_MAX_BYTES = 72

# Hash checked when the login does not exist, so the response time
# does not reveal whether an account exists.
_DUMMY_HASH = bcrypt.hashpw(b"", bcrypt.gensalt())


def authenticate_user(session: Session, login: str, password: str) -> User | None:
    """Check a user's login and password.

    Args:
        session (Session): The database session.
        login (str): The login entered.
        password (str): The password entered, in plain text.

    Returns:
        User | None: The user if the credentials are correct, otherwise None.
    """
    user = session.exec(select(User).where(User.login == login)).first()
    password_hash = user.password_hash.encode() if user else _DUMMY_HASH
    is_password_valid = bcrypt.checkpw(password.encode()[:BCRYPT_MAX_BYTES], password_hash)
    return user if user and is_password_valid else None


def create_token(sub: str) -> str:
    """Create a JWT token for a user.

    Args:
        sub (str): User id (token subject).

    Returns:
        str: The encoded token.
    """
    settings = get_jwt_settings()
    now = datetime.now(UTC)
    claims: dict[str, object] = {
        "sub": sub,
        "iss": ISSUER,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> int:
    """Decode a JWT token and return the user id.

    Args:
        token (str): The JWT token to decode.

    Returns:
        int: The user id (`sub`).

    Raises:
        HTTPException: If the token is invalid, expired, from another issuer or without a valid `sub`.
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
    except (InvalidTokenError, ValueError) as error:
        logger.info("JWT token rejected: %s", error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token invalide ou expiré.",
                "description": "Le token JWT fourni est invalide ou a expiré.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


# Rejects with 401 the requests without an `Authorization: Bearer <token>` header.
bearer_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> int:
    """Return the id of the logged-in user from the JWT token.

    To be used as a dependency of protected routes.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials extracted from the request.

    Returns:
        int: The id of the logged-in user.

    Raises:
        HTTPException: 401 if the token is missing, invalid or expired.
    """
    return decode_token(credentials.credentials)
