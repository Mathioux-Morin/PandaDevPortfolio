# Copyright (c) 2026 Mathieu MORIN, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Authentication token schema."""

from pydantic import BaseModel


class Token(BaseModel):
    """Access token returned after a successful login."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105
