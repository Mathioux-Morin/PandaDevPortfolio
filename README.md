# PandaDevPortfolio

Portfolio PandaDev : une API REST qui gère les données de chaque personne présentée, un site web pour les afficher et une base PostgreSQL.

## Structure du dépôt

| Dossier               | Contenu                                                       | Technologies                   |
|-----------------------|---------------------------------------------------------------|--------------------------------|
| [`api/`](api)         | API REST, authentification par login et mot de passe (JWT)    | Python 3.15, FastAPI, SQLModel |
| [`web/`](web)         | Site du portfolio (en cours de mise en place)                 | Nuxt 4, Nuxt UI, Bun           |
| [`bdd/`](bdd)         | Base de données et scripts d'initialisation                   | PostgreSQL 18, Docker Compose  |
| [`profile/`](profile) | Profils VS Code à importer (Python, Nuxt, SQL, Documentation) | VS Code                        |

## Démarrage rapide

Prérequis : [uv](https://docs.astral.sh/uv/), [Bun](https://bun.sh/) et Docker.

1. Lancer la base de données :

    ```bash
    cd bdd
    cp .env.example .env          # renseigner POSTGRES_PASSWORD
    docker compose up -d --build
    ```

2. Lancer l'API (renseigner `DATABASE_URL` et `JWT_SECRET_KEY` dans `api/.env`) :

    ```bash
    cd api
    cp .env.example .env
    uv sync
    uv run uvicorn my_api:app --env-file .env --reload
    ```

    La documentation Swagger est accessible à : `http://127.0.0.1:8000/docs`

Le détail de l'installation, de la configuration et des endpoints est dans [`api/README.md`](api/README.md).

## Licence

[MIT](LICENSE) © 2026 MORIN Mathieu, Mathias GARAIOS
