#!/bin/sh
set -e

# Só espera PostgreSQL se variável estiver definida
if [ -n "$POSTGRES_HOST" ]; then
  host="$POSTGRES_HOST"
  port="${POSTGRES_PORT:-5432}"

  echo "Aguardando PostgreSQL em $host:$port..."

  until python - <<PYTHON
import socket, os, time
host = os.environ.get('POSTGRES_HOST')
port = int(os.environ.get('POSTGRES_PORT', 5432))
try:
    sock = socket.create_connection((host, port), 2)
    sock.close()
    raise SystemExit(0)
except Exception:
    time.sleep(2)
    raise SystemExit(1)
PYTHON
  do
    sleep 1
  done
fi

echo "Executando migrações..."
poetry run python manage.py migrate --noinput

echo "Iniciando aplicação..."
exec "$@"
