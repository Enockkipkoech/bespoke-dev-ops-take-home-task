# ---- Build Stage ----
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY tsconfig.json ./
COPY src/ ./src/
COPY Dockerfile ./

RUN npm run build

# ---- Runtime Stage ----
FROM node:18-alpine AS runtime

WORKDIR /app

# tmux: required by terminus-2 agent to start terminal sessions
# bash, curl, python3, py3-pytest: required for solve.sh and test runner
RUN apk add --no-cache bash curl python3 py3-pip tmux && pip3 install pytest --break-system-packages

COPY package*.json ./
RUN npm ci --omit=dev

COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --chown=appuser:appgroup src/ ./src/
COPY --chown=appuser:appgroup k8s-deployment.yaml ./
COPY --chown=appuser:appgroup Dockerfile ./

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app
USER appuser

ENV PORT=3000
EXPOSE 3000

CMD ["node", "dist/index.js"]
