@echo off

cd .docker

if not exist .env (
    copy .env.example .env
    echo Environment file created from .env.example
)

docker-compose up --build -d
