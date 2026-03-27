# ---- Build Stage ----
FROM node:18-bookworm-slim AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY tsconfig.json ./tsconfig.json
COPY src/ ./src/

RUN npm run build

# ---- Runtime Stage ----
FROM node:18-bookworm-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    python3 \
    python3-pip \
    tmux \
    procps \
    ca-certificates \
    git \
    python3-pytest \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest --break-system-packages

COPY package*.json ./
RUN npm ci 

RUN groupadd -r appgroup && useradd -r -m -d /home/appuser -s /bin/bash -g appgroup appuser

RUN mkdir -p /tmp /tmp/tmux /home/appuser && \
    chown -R appuser:appgroup /home/appuser /tmp /tmp/tmux /app && \
    chmod 1777 /tmp /tmp/tmux

COPY --from=builder /app/dist ./dist
COPY tsconfig.json ./tsconfig.json
COPY src/ ./src/
COPY k8s-deployment.yaml ./k8s-deployment.yaml

USER appuser

ENV HOME=/home/appuser
ENV SHELL=/bin/bash
ENV TERM=xterm-256color
ENV TMPDIR=/tmp
ENV TMUX_TMPDIR=/tmp/tmux
ENV PORT=3000

EXPOSE 3000
CMD ["node", "dist/index.js"]