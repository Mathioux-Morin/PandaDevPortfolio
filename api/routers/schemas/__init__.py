# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Pydantic schemas of the API."""

from routers.schemas.token import Token
from routers.schemas.user import UserLogin

__all__ = [
    "Token",
    "UserLogin",
]
