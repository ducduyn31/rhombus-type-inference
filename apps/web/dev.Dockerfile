FROM node:20.2-slim as basenode

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

RUN apt-get update \
    && apt-get install -y vim bash make g++ \
    && pnpm install turbo --global \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM basenode as base

RUN apt-get update \
    && apt-get install -y software-properties-common build-essential zlib1g-dev libncurses5-dev  \
    libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev wget \
    && wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tar.xz -O /tmp/python.tar.xz \
    && tar -xf /tmp/python.tar.xz -C /tmp \
    && cd /tmp/Python-3.11.1 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && ln -s /usr/local/bin/python3.11 /usr/local/bin/python \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python \
    && ln -s /usr/local/bin/pip3.11 /usr/local/bin/pip \
    && pip install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*


FROM basenode as builder

WORKDIR /app

ARG APP

COPY ../.. .

RUN turbo prune --scope=$APP --docker

FROM basenode as installer

WORKDIR /app

ARG APP

COPY --from=builder /app/out/json/ .

COPY --from=builder /app/out/pnpm-lock.yaml /app/pnpm-lock.yaml

COPY apps/$APP/package.json /app/apps/$APP/package.json

RUN --mount=type=cache,id=pnpm,target=/pnpm/store,sharing=locked \
    pnpm install --frozen-lockfile

COPY --from=builder /app/out/full/ .

COPY ../../turbo.json turbo.json

RUN turbo run build --no-cache --filter=$APP^...

RUN --mount=type=cache,id=pnpm,target=/pnpm/store,sharing=locked \
    pnpm install --frozen-lockfile

FROM basenode as runner

WORKDIR /app

ARG APP
ARG START_DOMMAND=dev

COPY --from=installer /app .

CMD pnpm --filter=$APP run $START_DOMMAND
