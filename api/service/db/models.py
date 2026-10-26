# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Modèles ORM (tables SQL).

Les tables sont créées par les scripts de `bdd/init/`, pas par l'application.
"""

from sqlmodel import Field, SQLModel


class Utilisateur(SQLModel, table=True):
    """Personne pouvant se connecter à l'API."""

    __tablename__ = "utilisateurs"

    id: int | None = Field(default=None, primary_key=True)
    login: str = Field(unique=True)
    mot_de_passe: str  # Hash bcrypt généré par pgcrypto : crypt(..., gen_salt('bf'))
