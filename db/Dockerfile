# Portfolio PostgreSQL database, with the init scripts built in.
FROM postgres:18.6-alpine

# - gosu is only used by the entrypoint to switch from root to postgres: useless since the
#   container already runs as postgres (USER below), and it ships a vulnerable Go stdlib.
# - Alpine packages fixed upstream but not yet included in the official image.
# hadolint ignore=DL3018
RUN rm /usr/local/bin/gosu \
    && apk add --no-cache --upgrade brotli-libs libcurl

# Run in alphabetical order on first start, when the data volume is empty.
COPY --chmod=0444 init/ /docker-entrypoint-initdb.d/

# "postgres" user of the Alpine image (uid/gid 70).
USER 70:70

# TCP check (-h 127.0.0.1): during initialisation the temporary server only listens on the
# local socket, so the database is not reported ready before the scripts have finished.
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD ["sh", "-c", "pg_isready -h 127.0.0.1 -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\""]
