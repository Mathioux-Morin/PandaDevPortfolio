# Copyright (c) 2026 MORIN Mathieu, Mathias GARAIOS
# SPDX-License-Identifier: MIT
"""Point d'entrée principal de l'API du portfolio PandaDev.

Ce module initialise l'application FastAPI et enregistre les routeurs :
- Authentification : génération du token JWT
"""
from fastapi import FastAPI

from routers import authentication

description = """
## Authentification

Vous pouvez **générer un token JWT** (Bearer) requis pour accéder aux routes protégées,
à partir de votre login et de votre mot de passe.

## Type de données

Sauf indication contraire, les types de données utilisés dans cette API sont :

* `string` - Chaîne de caractères encodée en UTF-8
* `string($date)` - Date sous la forme `YYYY-MM-DD` (ex : `2024-01-15`, norme ISO-8601)
* `integer($int64)` - Entier sur 64 bits
* `number($double)` - Nombre à virgule flottante en double précision
* `boolean` - Booléen représenté par `true` ou `false`

## Code retour

* `20x` - L'opération s'est déroulée avec succès
* `404` - La ressource demandée n'existe pas.
  Dans le cas d'opérations retournant une liste, on recevra un code `200` avec une liste vide
* `422` - Au moins un des paramètres d'entrée est vide, malformé ou erroné
* `4xx` - Une erreur fonctionnelle s'est produite
* `50x` - Erreur technique rencontrée par le serveur
"""

app = FastAPI(
    title="API PandaDev Portfolio",
    summary="API de gestion des données de chaque personne du portfolio.",
    description=description,
    version="0.1.0",
    contact={
        "name": "Mathias GARAIOS",
        "email": "mathias.garaios@gmail.com",
    },
    # Derrière un reverse proxy sous le préfixe "/api" (ex : nginx), passer le préfixe
    # au serveur : `uv run uvicorn my_api:app --env-file .env --root-path /api`.
    )

app.include_router(authentication.router)


