#!/bin/bash
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: docker is not installed.' >&2
  exit 1
fi

if [ -z "$1" ]; then
  COMPOSE_POSTFIX="local"
else
  COMPOSE_POSTFIX=$1
fi


docker compose -f "docker/docker-compose-$COMPOSE_POSTFIX".yml up -d --build

echo "Users Service is up!"
echo ""
echo "Command to down all containers (may cause data loss):"
echo "/bin/bash local_down.sh"
echo ""