FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip wheel setuptools

COPY api_specs ./api_specs

COPY api_gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway/ .

RUN if [ -d "./api_specs" ]; then pip install ./api_specs; fi

# Переменные окружения
ENV HTTP_PORT=80
ENV HTTP_HOST=0.0.0.0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE ${HTTP_PORT}

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${HTTP_PORT}/ready || exit 1

CMD uvicorn main:app --host $HTTP_HOST --port $HTTP_PORT