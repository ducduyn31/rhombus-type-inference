FROM python:3.11-bookworm as basepython

ARG POETRY_DIR

RUN apt-get update && apt-get install -y bash gcc git  \
    libcurl4-openssl-dev libc-dev libpq-dev openssh-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_HOME="/opt/poetry" \
    VIRTUAL_ENV="/venv" \
    PYTHONPATH="/app:$PYTHONPATH"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry

RUN poetry config cache-dir $POETRY_DIR

FROM basepython as builder

RUN python -m venv $VIRTUAL_ENV

WORKDIR /app

COPY apps/backend/ ./

RUN --mount=type=cache,target=/root/.cache \
   poetry install --no-root

FROM basepython as runner

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

COPY configs/.pg_service.conf configs/.pgpass /root/

RUN chmod 600 /root/.pgpass

COPY apps/backend/scripts/entrypoint.sh /entrypoint.sh

WORKDIR /app

COPY --from=builder /app .

ENTRYPOINT ["/entrypoint.sh"]

CMD poetry run manage.py runserver
