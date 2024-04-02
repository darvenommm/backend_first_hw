#!/bin/bash

while read -r LINE; do
  if [[ $LINE == *'='* ]] && [[ $LINE != '#'* ]]; then
    ENV_VAR="$(echo $LINE | envsubst)"
    eval "declare $ENV_VAR"
  fi
done < .env

export DB_PORT=38000
export DB_HOST="127.0.0.1"

docker run -d --name for_alembic_revision_container \
        -e POSTGRES_PASSWORD=$DB_PASSWORD \
        -e POSTGRES_DB=$DB_NAME \
        -e POSTGRES_USER=$DB_USERNAME \
        -p $DB_PORT:5432 \
        -d postgres:16.2

sleep 2

alembic revision -m 'init: movies' --autogenerate

docker stop for_alembic_revision_container
docker rm for_alembic_revision_container
