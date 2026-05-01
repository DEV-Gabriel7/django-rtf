# Usar uma imagem Python Slim para otimização de espaço
FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

# Instalar dependências
RUN apt-get update && apt-get install --no-install-recommends -y \
        curl build-essential libpq-dev gcc libc-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependências primeiro (melhor cache)
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-dev

# Copiar projeto
COPY . .

# Coletar arquivos estáticos
RUN poetry run python manage.py collectstatic --noinput

# Entrypoint (migrations)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# 🔥 IMPORTANTE: usar Gunicorn + $PORT
CMD ["sh", "-c", "poetry run gunicorn bookstore.wsgi:application --bind 0.0.0.0:$PORT"]