FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /usr/local/bin/uv
# A job's image must have sh and git: its code is fetched into /workspace/code at start, so the environment lives outside /workspace.
# curl: a job on rented compute (vast.ai, Runpod) runs under a supervisor that needs it.
# A job on NVIDIA GPUs needs nothing more here: the node brings the driver, and torch from PyPI
# (uv add torch) brings CUDA, on amd64 and arm64 alike.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv PATH=/opt/venv/bin:$PATH
WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev
