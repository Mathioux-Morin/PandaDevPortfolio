# Base PostgreSQL du portfolio, avec les scripts d'initialisation intégrés.
FROM postgres:18.6-alpine

# - gosu ne sert qu'à l'entrypoint pour passer de root à postgres : inutile puisque le conteneur
#   tourne directement en postgres (USER plus bas), et il embarque une stdlib Go vulnérable.
# - Paquets Alpine corrigés en amont mais pas encore intégrés à l'image officielle.
# hadolint ignore=DL3018
RUN rm /usr/local/bin/gosu \
    && apk add --no-cache --upgrade brotli-libs libcurl

# Exécutés par ordre alphabétique au premier démarrage, quand le volume de données est vide.
COPY --chmod=0444 init/ /docker-entrypoint-initdb.d/

# Utilisateur "postgres" de l'image Alpine (uid/gid 70).
USER 70:70

# Vérification en TCP (-h 127.0.0.1) : pendant l'initialisation, le serveur temporaire n'écoute
# que sur le socket local, la base n'est donc pas déclarée prête avant la fin des scripts.
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD ["sh", "-c", "pg_isready -h 127.0.0.1 -U \"$POSTGRES_USER\" -d \"$POSTGRES_DB\""]
