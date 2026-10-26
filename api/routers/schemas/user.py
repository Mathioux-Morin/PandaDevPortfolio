# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""User data schemas."""

from pydantic import BaseModel, ConfigDict, SecretStr


class UserLogin(BaseModel):
    """Credentials sent to the authentication route."""

    model_config = ConfigDict(extra="forbid")

    login: str
    password: SecretStr
