#!/bin/sh
set -e

host="$POSTGRES_HOST"
port="$POSTGRES_PORT"

if [ -z "$host" ]; then
  host=db
fi

if [ -z "$port" ]; then
  port=5432
fi

echo "Aguardando PostgreSQL em $host:$port..."

until python - <<PYTHON
import socket, os, time
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', 5432))
try:
    sock = socket.create_connection((host, port), 2)
    sock.close()
    print('PostgreSQL disponível')
    raise SystemExit(0)
except Exception:
    print('PostgreSQL não disponível, aguardando...')
    time.sleep(2)
    raise SystemExit(1)
PYTHON
 do
  sleep 1
done

echo "Executando migrações..."
poetry run python manage.py migrate --noinput

echo "Iniciando aplicação..."
exec "$@"
