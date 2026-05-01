# 📚 Bookstore API - Deploy com Heroku

API desenvolvida com **Django + Django REST Framework**, preparada para deploy utilizando Docker no Heroku e integração com CI/CD via GitHub Actions.

---

## 🚀 Tecnologias utilizadas

* Python 3
* Django
* Django REST Framework
* Gunicorn
* Whitenoise
* Docker
* GitHub Actions

---

## ⚙️ Configurações para produção

O projeto foi ajustado para rodar em ambiente de produção com as seguintes configurações:

* Uso de `gunicorn` como servidor WSGI
* Uso de `whitenoise` para servir arquivos estáticos
* Variáveis de ambiente para segurança:

  * `SECRET_KEY`
  * `DEBUG`
  * `DJANGO_ALLOWED_HOSTS`
* Configuração de `ALLOWED_HOSTS`
* Uso de `STATIC_ROOT` e `CompressedManifestStaticFilesStorage`

---

## 🐳 Deploy com Docker + Heroku

O projeto está configurado para deploy utilizando containers Docker no Heroku.

### Arquivos utilizados:

* `Dockerfile`
* `heroku.yml`
* `.dockerignore`

### heroku.yml

```yaml
build:
  docker:
    web: Dockerfile

run:
  web: gunicorn bookstore.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🔐 Variáveis de ambiente

Exemplo de configuração no Heroku:

```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=0
heroku config:set DJANGO_ALLOWED_HOSTS=seu-app.herokuapp.com
```

---

## 🔄 CI/CD com GitHub Actions

O projeto possui integração com GitHub Actions para automação de deploy.

### Workflow:

* Build da imagem Docker
* Push para o registry do Heroku
* Release automático da aplicação

Arquivo:

```
.github/workflows/deploy.yml
```

---

## 🗄️ Banco de dados

Por padrão, o projeto utiliza SQLite para desenvolvimento.

Em produção, pode ser configurado para PostgreSQL via variáveis de ambiente.

---

## ▶️ Executando o projeto localmente

```bash
# instalar dependências
poetry install

# rodar migrations
python manage.py migrate

# iniciar servidor
python manage.py runserver
```

---

## ⚠️ Observação importante

Não foi possível concluir o deploy final no Heroku devido à exigência de verificação de conta com cartão de crédito/débito.

Erro encontrado:

```
Error: verification_required
```

Apesar disso:

✔ Toda a estrutura de deploy está configurada
✔ O projeto está pronto para produção
✔ O pipeline de CI/CD está implementado

---

## 📌 Conclusão

Este projeto demonstra:

* Configuração de uma API Django para produção
* Containerização com Docker
* Preparação para deploy em cloud
* Integração com CI/CD

---

## 👨‍💻 Autor

Gabriel Ribeiro Ferreira

