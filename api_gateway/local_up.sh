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

echo "Local machine is up!"
echo ""
echo "You can check API docs at: http://MACHINE_IP:8080/docs"
echo ""
echo "Command to down all containers (may cause data loss):"
echo "/bin/bash local_down.sh"
echo ""
echo ""
