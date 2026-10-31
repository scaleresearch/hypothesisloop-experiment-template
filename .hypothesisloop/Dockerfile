FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv
# A job's image must have sh and git: its code is fetched into /workspace/code at start, so the environment lives outside /workspace.
# It also carries every program `hl capacity` lists under image_needs (curl, for jobs on rented machines).
ENV UV_PROJECT_ENVIRONMENT=/opt/venv PATH=/opt/venv/bin:$PATH
WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
