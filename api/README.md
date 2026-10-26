# PandaDev Portfolio — REST API

FastAPI REST API of the PandaDev portfolio. It manages the data of each person shown in the portfolio and authenticates people with a login and password (JWT token).

## Table of contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Database](#database)
4. [Configuration](#configuration)
5. [Running](#running)
6. [Code quality](#code-quality)
7. [Architecture](#architecture)
8. [Endpoints](#endpoints)
   1. [Authentication](#authentication)
   2. [Protected routes](#protected-routes)

---

## Requirements

* Python 3.15 or later
* [uv](https://docs.astral.sh/uv/) (package manager)
* Docker (for the PostgreSQL database, see [`db/`](../db))

---

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd PandaDevPortfolio/api
    ```

2. Install the dependencies:

    ```bash
    uv sync
    ```

3. Create and fill in the environment file (see [Configuration](#configuration)):

    ```bash
    cp .env.example .env
    ```

---

## Database

The PostgreSQL 18 database runs in a container defined in [`db/`](../db). The scripts in [`db/init/`](../db/init) create the tables on first start.

```bash
cd ../db
cp .env.example .env          # fill in POSTGRES_PASSWORD
docker compose up -d --build
docker compose ps             # wait for the "healthy" status
```

> **Notes:**
>
> * If port `5432` is already in use (another PostgreSQL), change `POSTGRES_PORT` in `db/.env` and the port of `DATABASE_URL` in `api/.env` (e.g. `5433`).
> * The init scripts only run when the data volume is empty. To run them again: `docker compose down -v` (**deletes all data**).

### `users`

People allowed to log in. Accounts are not created through the API: they are added directly in the database.

| Column          | Type          | Description                                  |
|-----------------|---------------|----------------------------------------------|
| `id`            | integer (PK)  | Auto-incremented id, carried by the token    |
| `login`         | text (unique) | Login                                        |
| `password_hash` | text          | bcrypt hash of the password (via `pgcrypto`) |

**Add a user:**

```bash
docker compose exec db psql -U portfolio -d portfolio
```

```sql
INSERT INTO users (login, password_hash)
VALUES ('jdoe', crypt('password', gen_salt('bf', 12)));
```

> **Note:** bcrypt only uses the first 72 bytes of the password.

---

## Configuration

All variables live in `.env`:

| Variable                          | Description                                        | Example                                                    |
|-----------------------------------|----------------------------------------------------|------------------------------------------------------------|
| `DATABASE_URL`                    | PostgreSQL connection URL (`postgresql://` format) | `postgresql://portfolio:password@localhost:5432/portfolio` |
| `JWT_SECRET_KEY`                  | Secret key used to sign the JWT tokens             | `openssl rand -hex 32`                                     |
| `JWT_ALGORITHM`                   | JWT signing algorithm (default: `HS256`)           | `HS256`                                                    |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes (default: `30`)          | `30`                                                       |

`DATABASE_URL` uses the values of `db/.env`: `postgresql://POSTGRES_USER:POSTGRES_PASSWORD@localhost:POSTGRES_PORT/POSTGRES_DB`.

> ⚠️ **Warning:** Never share your `.env` file.

---

## Running

```bash
# Development (auto-reload)
uv run uvicorn my_api:app --env-file .env --reload

# Production, behind a reverse proxy serving the API under /api (e.g. nginx)
uv run uvicorn my_api:app --env-file .env --root-path /api
```

The interactive Swagger documentation is available at: `http://127.0.0.1:8000/docs`

> **Note:** User-facing texts (Swagger description, error messages) are written in French.

---

## Code quality

```bash
uv run ruff check     # linter
uv run ty check       # type checking
uv run pytest         # tests
```

---

## Architecture

```text
.
├── my_api.py                        # FastAPI entry point
├── pyproject.toml                   # Project dependencies and metadata (uv)
├── ruff.toml                        # Ruff linter configuration
├── routers/                         # Router layer (HTTP)
│   ├── authentication.py            # JWT authentication route
│   └── schemas/                     # Pydantic request and response models
│       ├── token.py                 # Token schema
│       └── user.py                  # Login credentials (UserLogin)
├── service/                         # Business layer
│   ├── auth/
│   │   └── security.py              # bcrypt check, JWT token creation and decoding
│   ├── db/                          # Database access (PostgreSQL / SQLModel)
│   │   ├── database.py              # Engine and session management
│   │   └── models.py                # ORM models (SQL tables)
│   └── settings/                    # Environment variable loading
│       ├── auth.py
│       └── database.py
└── tests/                           # pytest tests (in-memory SQLite database)
```

---

## Endpoints

### Authentication

Issues the JWT token required to access protected routes.

| Method | Path          | Description                              | Code      |
|--------|---------------|------------------------------------------|-----------|
| POST   | `/auth/token` | Issues a token from a login and password | 200 / 401 |

**`POST /auth/token` body:**

```json
{
  "login": "jdoe",
  "password": "password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Error codes: `401` (wrong login or password), `422` (invalid body).

The token only carries the user id:

| Claim | Description                  |
|-------|------------------------------|
| `sub` | User id (`users.id`)         |
| `iss` | Issuer: `pandadev-portfolio` |
| `iat` | Issued at                    |
| `exp` | Expiration date              |

---

### Protected routes

Protected routes expect the `Authorization: Bearer <token>` header. The `get_current_user_id` dependency provides the id of the logged-in user:

```python
from typing import Annotated

from fastapi import Depends

from service.auth.security import get_current_user_id


@router.get("/me")
async def read_me(user_id: Annotated[int, Depends(get_current_user_id)]) -> dict[str, int]:
    return {"id": user_id}
```

Error codes: `401` (missing, invalid or expired token, or token from another issuer).
