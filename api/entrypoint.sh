#!/bin/bash
set -e

# PostgreSQLが起動するのを待つ
while ! /usr/bin/nc -z postgresql 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "PostgreSQL started"

# Djangoマイグレーションを実行
# python manage.py migrate

# Djangoサーバーを起動
# exec python manage.py runserver 0.0.0.0:8000



