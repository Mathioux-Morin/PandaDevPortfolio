# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Configuration JWT."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    """Paramètres pour la gestion des tokens JWT."""

    model_config = SettingsConfigDict(env_prefix="JWT_")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


def get_jwt_settings() -> JwtSettings:
    """Récupère les paramètres JWT à partir des variables d'environnement."""
    return JwtSettings()
