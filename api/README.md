# PandaDev Portfolio — API REST

API REST FastAPI du portfolio PandaDev. Elle gère les données de chaque personne présentée dans le portfolio et authentifie les personnes par login et mot de passe (token JWT).

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Base de données](#base-de-données)
4. [Configuration](#configuration)
5. [Lancement](#lancement)
6. [Qualité du code](#qualité-du-code)
7. [Architecture](#architecture)
8. [Endpoints](#endpoints)
   1. [Authentification](#authentification)
   2. [Routes protégées](#routes-protégées)

---

## Prérequis

* Python 3.15 ou supérieur
* [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets)
* Docker (pour la base PostgreSQL, voir [`bdd/`](../bdd))

---

## Installation

1. Cloner le dépôt :

    ```bash
    git clone https://github.com/Mathioux-Morin/PandaDevPortfolio.git
    cd PandaDevPortfolio/api
    ```

2. Installer les dépendances :

    ```bash
    uv syncrefa
    ```

3. Créer et remplir le fichier d'environnement (voir [Configuration](#configuration)) :

    ```bash
    cp .env.example .env
    ```

---

## Base de données

La base PostgreSQL 18 tourne dans un conteneur défini dans [`bdd/`](../bdd). Les scripts de [`bdd/init/`](../bdd/init) créent les tables au premier démarrage.

```bash
cd ../bdd
cp .env.example .env          # renseigner POSTGRES_PASSWORD
docker compose up -d --build
docker compose ps             # attendre l'état "healthy"
```

> **Notes :**
>
> * Si le port `5432` est déjà utilisé (autre PostgreSQL), changer `POSTGRES_PORT` dans `bdd/.env` et le port de `DATABASE_URL` dans `api/.env` (ex : `5433`).
> * Les scripts d'initialisation ne s'exécutent que si le volume de données est vide. Pour les rejouer : `docker compose down -v` (**efface toutes les données**).

### `utilisateurs`

Personnes autorisées à se connecter. Il n'y a pas de création de compte via l'API : les comptes sont ajoutés directement en base.

| Colonne        | Type          | Description                                   |
|----------------|---------------|-----------------------------------------------|
| `id`           | integer (PK)  | Identifiant auto-incrémenté, contenu du token |
| `login`        | text (unique) | Identifiant de connexion                      |
| `mot_de_passe` | text          | Hash bcrypt du mot de passe (via `pgcrypto`)  |

**Ajouter une personne :**

```bash
docker compose exec bdd psql -U portfolio -d portfolio
```

```sql
INSERT INTO utilisateurs (login, mot_de_passe)
VALUES ('jdoe', crypt('mot de passe', gen_salt('bf', 12)));
```

> **Note :** bcrypt ne prend en compte que les 72 premiers octets du mot de passe.

---

## Configuration

Toutes les variables sont dans `.env` :

| Variable                          | Description                                           | Exemple                                                      |
|-----------------------------------|-------------------------------------------------------|--------------------------------------------------------------|
| `DATABASE_URL`                    | URL de connexion PostgreSQL (format `postgresql://`)  | `postgresql://portfolio:motdepasse@localhost:5432/portfolio` |
| `JWT_SECRET_KEY`                  | Clé secrète pour signer les tokens JWT                | `openssl rand -hex 32`                                       |
| `JWT_ALGORITHM`                   | Algorithme de signature JWT (défaut : `HS256`)        | `HS256`                                                      |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de validité du token en minutes (défaut : `30`) | `30`                                                         |

`DATABASE_URL` reprend les valeurs de `bdd/.env` : `postgresql://POSTGRES_USER:POSTGRES_PASSWORD@localhost:POSTGRES_PORT/POSTGRES_DB`.

> ⚠️ **Attention :** Ne partagez jamais votre fichier `.env`.

---

## Lancement

```bash
# Développement (rechargement automatique)
uv run uvicorn my_api:app --env-file .env --reload

# Production, derrière un reverse proxy servant l'API sous /api (ex : nginx)
uv run uvicorn my_api:app --env-file .env --root-path /api
```

La documentation interactive Swagger est accessible à : `http://127.0.0.1:8000/docs`

---

## Qualité du code

```bash
uv run ruff check     # linter
uv run ty check       # vérification des types
uv run pytest         # tests
```

---

## Architecture

```text
.
├── my_api.py                        # Point d'entrée FastAPI
├── pyproject.toml                   # Dépendances et métadonnées du projet (uv)
├── ruff.toml                        # Configuration du linter Ruff
├── routers/                         # Couche routeurs (HTTP)
│   ├── authentication.py            # Route d'authentification JWT
│   └── schemas/                     # Modèles Pydantic des requêtes et réponses
│       ├── token.py                 # Schéma du token
│       └── user.py                  # Identifiants de connexion (UserLogin)
└── service/                         # Couche métier
    ├── auth/
    │   └── security.py              # Vérification bcrypt, création et décodage des tokens JWT
    ├── db/                          # Accès base de données (PostgreSQL / SQLModel)
    │   ├── database.py              # Moteur et gestion des sessions
    │   └── models.py                # Modèles ORM (tables SQL)
    └── settings/                    # Chargement des variables d'environnement
        ├── auth.py
        └── database.py
```

---

## Endpoints

### Authentification

Génération du token JWT requis pour accéder aux routes protégées.

| Méthode | Chemin        | Description                                         | Code      |
|---------|---------------|-----------------------------------------------------|-----------|
| POST    | `/auth/token` | Génère un token à partir d'un login et mot de passe | 200 / 401 |

**Corps `POST /auth/token` :**

```json
{
  "login": "jdoe",
  "password": "mot de passe"
}
```

**Réponse :**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Codes d'erreur : `401` (login ou mot de passe incorrect), `422` (corps invalide).

Le token ne contient que l'identifiant de la personne :

| Claim | Description                                    |
|-------|------------------------------------------------|
| `sub` | Identifiant de la personne (`utilisateurs.id`) |
| `iss` | Émetteur : `pandadev-portfolio`                |
| `iat` | Date d'émission                                |
| `exp` | Date d'expiration                              |

---

### Routes protégées

Les routes protégées attendent l'en-tête `Authorization: Bearer <token>`. La dépendance `get_current_user_id` fournit l'identifiant de la personne connectée :

```python
from typing import Annotated

from fastapi import Depends

from service.auth.security import get_current_user_id


@router.get("/moi")
async def read_me(user_id: Annotated[int, Depends(get_current_user_id)]) -> dict[str, int]:
    return {"id": user_id}
```

Codes d'erreur : `401` (token absent, invalide, expiré ou d'un autre émetteur).
