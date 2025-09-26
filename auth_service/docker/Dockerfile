FROM python:3.11

WORKDIR /usr/src/app

RUN pip install --upgrade pip wheel setuptools

COPY api_specs ./api_specs

COPY auth_service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY auth_service ./

ENTRYPOINT ["python", "main.py"]
CMD []