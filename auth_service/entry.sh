#!/bin/bash
if [[ "$APP_ENV" == "TESTING" ]]; then
    export $(grep -v '^#' .env.testing | xargs -d '\r')
elif [[ "$APP_ENV" == "LOCAL" ]]; then
    export $(grep -v '^#' .env.local | xargs -d '\r')
fi
alembic upgrade head
exec python /usr/src/app/main.py