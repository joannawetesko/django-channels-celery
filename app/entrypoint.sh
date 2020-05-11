#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for the database..."

  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done
  echo "Database started"
fi

echo "Waiting for redis..."

  while ! nc -z "$REDIS_HOST" "$REDIS_PORT"; do
    sleep 0.1
  done
  echo "Redis started"

exec "$@"