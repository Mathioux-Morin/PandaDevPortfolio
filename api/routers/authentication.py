# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Authentication route that issues JWT access tokens."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
lazy from sqlmodel import Session

from routers.schemas import Token, UserLogin
from service.auth.security import authenticate_user, create_token
from service.db.database import get_session

# Tags, summaries, descriptions and examples are shown in Swagger: they stay in French.
router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post(
    "/token",
    summary="Génère un token d'accès à partir d'un login et d'un mot de passe",
    description=(
        "Génère un token d'accès JWT si le login et le mot de passe correspondent à une personne en base.\n\n"
        "- Le token ne contient que l'identifiant de la personne (`sub`)."
    ),
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Login ou mot de passe incorrect.",
        },
    },
)
def login_for_access_token(
    credentials: Annotated[
        UserLogin,
        Body(
            openapi_examples={
                "login": {
                    "summary": "Exemple de connexion",
                    "value": {
                        "login": "jdoe",
                        "password": "mot de passe",
                    },
                },
            },
        ),
    ],
    session: Annotated[Session, Depends(get_session)],
) -> Token:
    """Issue a JWT access token when the login and password match a user in the database."""
    # Synchronous route (`def`): the bcrypt check and the SQL query are blocking,
    # so FastAPI runs it in a separate thread.
    user = authenticate_user(session, credentials.login, credentials.password.get_secret_value())
    if user is None or user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Identifiants invalides.",
                "description": "Login ou mot de passe incorrect.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=create_token(sub=str(user.id)))
