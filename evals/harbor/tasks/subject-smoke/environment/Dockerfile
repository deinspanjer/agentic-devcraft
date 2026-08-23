FROM node:24@sha256:934240a162082fd8b8a2f90cd5114446443f1eba1c5378f6687167ca405e6584

COPY --from=ghcr.io/astral-sh/uv@sha256:cf4eedcaa81655197f625739489effcbe71b61ceb1506f332c3facae5deceded /uv /uvx /bin/

RUN npm install --global @anthropic-ai/claude-code@2.1.239 @openai/codex@0.149.0 skills@1.5.9 \
    && mkdir -p /app \
    && chown node:node /app

WORKDIR /app
