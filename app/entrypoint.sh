#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for the database..."

  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done
  echo "Database started"
fi

echo "Waiting for rabbitMQ"

  while ! nc -z "$RABBIT_HOST" "$RABBIT_PORT"; do
    sleep 0.1
  done
  echo "rabbitMQ started"

exec "$@"