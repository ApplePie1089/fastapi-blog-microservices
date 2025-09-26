#!/bin/bash
if [ -z "${1}" ]; then
  COMPOSE_POSTFIX="local"
else
  COMPOSE_POSTFIX=$1
fi
docker compose -f "docker/docker-compose-$COMPOSE_POSTFIX.yml" down
