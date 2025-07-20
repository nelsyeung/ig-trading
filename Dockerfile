# syntax=docker/dockerfile:1
FROM ubuntu:26.04 AS base
USER 1000:1000
WORKDIR /workdir
COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /uvx /bin/
COPY .python-version README.md pyproject.toml uv.lock ./
COPY src ./src
COPY --chmod=755 <<EOF /entrypoint.sh
#!/bin/bash
. .venv/bin/activate
exec "\$@"
EOF

RUN uv sync --locked --no-cache --no-dev
ENTRYPOINT ["/entrypoint.sh"]

FROM base AS dev
USER 0:0
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get --assume-yes update && \
    apt-get --assume-yes full-upgrade && \
    apt-get install --assume-yes --no-install-recommends \
        ca-certificates=20260223 \
        curl=8.18.0* \
        git=1:2.53.0* \
        sudo=1.9.17* && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install --assume-yes --no-install-recommends \
        nodejs=24.13.0* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    usermod --append --groups sudo ubuntu && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    npm install --global markdownlint-cli2@"0.23.2"
USER 1000:1000
COPY --from=hadolint/hadolint:v2.15.1-alpine /bin/hadolint /bin/
RUN uv sync --locked
# The SHELL environment variable must match CMD. By default, running /bin/bash
# only sets SHELL for that process and does not export it, so subprocesses (like
# Vim or Python) may not see the correct SHELL. Explicitly setting ENV SHELL
# ensures consistency across subprocesses.
ENV SHELL=/bin/bash
CMD ["/bin/bash"]

FROM dev AS vim
USER 0:0
RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends \
        vim-gtk3=2:9.1.2141* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
USER 1000:1000
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="~/.local/bin:$PATH"
RUN mkdir ~/.config
