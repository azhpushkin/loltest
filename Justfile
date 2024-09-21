# set dotenv-load

user := `id -u` + ":" + `id -g`
docker-exec := "docker compose exec -u " + user


db:
    docker-compose up -d db

run: db
    docker-compose up -d web

res: db
    docker-compose restart web
    docker-compose restart worker

logs:
    docker-compose logs -f worker

shell:
    {{docker-exec}} web bash

pyshell:
    {{docker-exec}} web python manage.py shell

dbshell:
    {{docker-exec}} db psql -U $POSTGRES_USER

test:
    {{docker-exec}} web pytest

# fix:
#     black .
#     isort .
#     ruff check --fix .

compile:
    pip-compile requirements.in --resolver=backtracking > requirements.txt

sim file:
    cd simulation && python serve.py {{file}}

m:
    {{docker-exec}} web python manage.py makemigrations
    {{docker-exec}} web python manage.py migrate
