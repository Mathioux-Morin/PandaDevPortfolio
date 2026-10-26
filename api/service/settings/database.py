# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""PostgreSQL database settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
lazy from pydantic import PostgresDsn


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    url: PostgresDsn


def get_database_settings() -> DatabaseSettings:
    """Read the database settings from the environment variables."""
    return DatabaseSettings()
