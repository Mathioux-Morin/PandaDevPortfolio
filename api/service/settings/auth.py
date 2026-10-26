# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""JWT settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    """JWT token settings."""

    model_config = SettingsConfigDict(env_prefix="JWT_")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


def get_jwt_settings() -> JwtSettings:
    """Read the JWT settings from the environment variables."""
    return JwtSettings()
