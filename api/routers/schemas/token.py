# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Schema de donnée pour les tokens d'authentification."""

from pydantic import BaseModel


class Token(BaseModel):
    """Model pour les tokens d'authentification."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105
