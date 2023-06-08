#!/bin/bash

echo "Waiting for postgres..."

RETRIES=5

until psql -h "$PG_HOST" -U "$PG_USER" -d "$PG_DB" -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

echo "PostgreSQL started"

exec "$@"
