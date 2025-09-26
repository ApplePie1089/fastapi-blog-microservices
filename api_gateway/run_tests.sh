if ! [ -x "$(command -v docker-compose)" ]; then   alias docker-compose="docker compose"; fi
./local_up.sh tests
docker exec api-gateway-testing /bin/bash wait_for_start.sh
docker exec api-gateway-testing pytest tests/functional
./local_down.sh tests