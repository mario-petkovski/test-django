#!/bin/bash

until pg_isready -h postgres -p 5432 -U postgres; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "PostgreSQL is ready!"

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
