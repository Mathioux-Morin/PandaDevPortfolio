# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Configuration de la base de données PostgreSQL."""

from pydantic_settings import BaseSettings, SettingsConfigDict
lazy from pydantic import PostgresDsn


class DatabaseSettings(BaseSettings):
    """Paramètres de connexion à la base de données."""

    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    url: PostgresDsn


def get_database_settings() -> DatabaseSettings:
    """Récupère les paramètres de la base de données à partir des variables d'environnement."""
    return DatabaseSettings()
