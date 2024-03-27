FROM node:20.2-slim as base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

RUN apt-get update \
    && apt-get install -y vim bash python3 make g++ \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && pnpm install turbo --global \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

FROM base as builder

WORKDIR /app

ARG APP

COPY . .

RUN turbo prune --scope=$APP --docker

FROM base as installer

WORKDIR /app

ARG APP

COPY --from=builder /app/out/json/ .

COPY --from=builder /app/out/pnpm-lock.yaml /app/pnpm-lock.yaml

COPY apps/$APP/package.json /app/apps/$APP/package.json

RUN --mount=type=cache,id=pnpm,target=/pnpm/store,sharing=locked \
    pnpm install --frozen-lockfile

COPY --from=builder /app/out/full/ .

COPY turbo.json turbo.json

RUN turbo run build --no-cache --filter=$APP^...

RUN --mount=type=cache,id=pnpm,target=/pnpm/store,sharing=locked \
    pnpm install --frozen-lockfile

FROM base as runner

WORKDIR /app

ARG APP
ARG START_DOMMAND=dev

COPY --from=installer /app .

CMD pnpm --filter=$APP run $START_DOMMAND
