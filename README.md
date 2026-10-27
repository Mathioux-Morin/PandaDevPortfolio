# PandaDevPortfolio

PandaDev portfolio: a REST API that manages the data of each person shown, a website to display it, and a PostgreSQL database.

## Repository layout

| Folder                | Content                                                       | Stack                          |
|-----------------------|---------------------------------------------------------------|--------------------------------|
| [`api/`](api)         | REST API, login and password authentication (JWT)             | Python 3.15, FastAPI, SQLModel |
| [`web/`](web)         | Public portfolio website and private login area               | Nuxt 4, Nuxt UI, Bun           |
| [`db/`](db)           | Database and init scripts                                     | PostgreSQL 18, Docker Compose  |
| [`profile/`](profile) | VS Code profiles to import (Python, Nuxt, SQL, Documentation) | VS Code                        |

## Quick start

Requirements: [uv](https://docs.astral.sh/uv/), [Bun](https://bun.sh/) and Docker.

1. Start the database:

    ```bash
    cd db
    cp .env.example .env          # fill in POSTGRES_PASSWORD
    docker compose up -d --build
    ```

2. Start the API (fill in `DATABASE_URL` and `JWT_SECRET_KEY` in `api/.env`):

    ```bash
    cd api
    cp .env.example .env
    uv sync
    uv run uvicorn my_api:app --env-file .env --reload
    ```

    The Swagger documentation is available at: `http://127.0.0.1:8000/docs`

3. Start the website (fill in `NUXT_SESSION_PASSWORD` in `web/.env`):

    ```bash
    cd web
    cp .env.example .env
    bun install
    bun run dev
    ```

    The website is available at: `http://localhost:3000` (private area: `/login`)

Installation, configuration and endpoint details are in [`api/README.md`](api/README.md).

## Conventions

Code, file names, comments and documentation are in English.

* **Website**: texts are translated with `@nuxtjs/i18n`, in [`web/i18n/locales/`](web/i18n/locales) (`fr.json`, `en.json`). French is the default locale (`/login`), other locales get a URL prefix (`/en/login`). Never write a user-facing text directly in a component: add a key to every locale file.
* **API**: texts shown in Swagger and API error messages are in French. The website does not display them as is: the Nuxt server returns an error code (e.g. `invalid_credentials`) that the page translates.

## License

[MIT](LICENSE) © 2026 MORIN Mathieu, Mathias GARAIOS
