# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Schémas qui définissent les données d'un utilisateur."""

from pydantic import BaseModel, ConfigDict, SecretStr


class UserLogin(BaseModel):
    """Identifiants envoyés à la route d'authentification."""

    model_config = ConfigDict(extra="forbid")

    login: str
    password: SecretStr
