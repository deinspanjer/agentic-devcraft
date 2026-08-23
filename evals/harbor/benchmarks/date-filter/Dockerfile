FROM node:24@sha256:934240a162082fd8b8a2f90cd5114446443f1eba1c5378f6687167ca405e6584 AS node

RUN npm install --global @openai/codex@0.149.0

FROM python:3.14.0-slim-bookworm@sha256:d13fa0424035d290decef3d575cea23d1b7d5952cdf429df8f5542c71e961576

COPY --from=node /usr/local/ /usr/local/

RUN useradd --create-home --uid 1000 node \
    && mkdir -p /app \
    && chown node:node /app

WORKDIR /app

COPY --chown=node:node workspace/ /app/
