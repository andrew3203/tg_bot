# list of commands for local develepment
default:
  just --list

# up docker
up:
  docker-compose -f local.yml up

# up docker in a background
up-d:
  docker-compose -f local.yml up -d

# build docker images
build:
  docker-compose -f local.yml --build

# build and run docker images
run:
  docker-compose -f local.yml up --build

# build and run docker images in a background
run-d:
  docker-compose -f local.yml up -d --build

# show logs of all services or of specific service
logs *args:
  docker-compose -f local.yml logs {{args}} -f

# stop docker porccess
down:
  docker-compose -f local.yml down

# stop docker porccess and rm voluems
down-v:
  docker-compose -f local.yml down -v

# docker compose kill
kill:
  docker-compose -f local.yml kill

# docker ps
ps:
  docker-compose -f local.yml ps

# run some command in fast api
exec *args:
  docker-compose -f local.yml exec fastapi {{args}}

# run make migrations, `args` - is a text of revision
mm *args:
  docker-compose -f local.yml exec fastapi alembic revision --autogenerate -m "{{args}}"

# run migrate (applies migrations)
migrate:
  docker-compose -f local.yml exec fastapi alembic upgrade head

# run current (chec if migrations applyed)
acurrent:
  docker-compose -f local.yml exec fastapi alembic current

# downgrade migrations to `args` version, use args='head' to downgrade to prev version
downgrade *args:
  docker-compose -f local.yml exec fastapi alembic downgrade {{args}}

# run bcack formating
black:
  docker-compose -f local.yml exec fastapi black app

# testing for FastAPI to run tests, args: `-s` for example
pytest:
  docker-compose -f local.yml exec fastapi pytest

# testing for FastAPI file, to run tests, args: `path/to/file -s` for example
test_file *args:
  docker exec -it app_local_fastapi pytest {{args}}

# run mypy
mypy:
  just exec mypy app

# run black and  linter
lint:
  just black
  just mypy
  pre-commit
