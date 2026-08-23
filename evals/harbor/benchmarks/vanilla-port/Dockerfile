FROM node:24@sha256:934240a162082fd8b8a2f90cd5114446443f1eba1c5378f6687167ca405e6584 AS node

RUN npm install --global @openai/codex@0.149.0

FROM rust:1.88.0-bookworm@sha256:af306cfa71d987911a781c37b59d7d67d934f49684058f96cf72079c3626bfe0

COPY --from=node /usr/local/ /usr/local/

RUN rustup component add rustfmt clippy

RUN useradd --create-home --uid 1000 node \
    && ln -s /usr/local/cargo/bin/cargo /usr/local/bin/cargo \
    && ln -s /usr/local/cargo/bin/rustc /usr/local/bin/rustc \
    && ln -s /usr/local/cargo/bin/rustup /usr/local/bin/rustup \
    && mkdir -p /app \
    && chown node:node /app

WORKDIR /app

COPY --chown=node:node workspace/ /app/
