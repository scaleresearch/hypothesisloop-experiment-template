FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv
# The job's code is fetched into /workspace/code at start, so the environment lives outside /workspace.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv PATH=/opt/venv/bin:$PATH
WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
