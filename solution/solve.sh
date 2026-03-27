#!/usr/bin/env bash
set -euo pipefail

score=0

add_score () {
  score=$(python3 - <<PY
s=float("$score")
print(s + $1)
PY
)
}

# ---------------- Dockerfile (0.4) ----------------
grep -q 'ENV PORT=3000' /app/Dockerfile && add_score 0.10
grep -q 'EXPOSE 3000' /app/Dockerfile && add_score 0.05
grep -q 'AS builder' /app/Dockerfile && add_score 0.10
grep -q 'npm ci --omit=dev' /app/Dockerfile && add_score 0.15

# ---------------- App (0.2) ----------------
grep -q 'process.env.PORT' /app/src/index.ts && add_score 0.05
grep -q '/healthz' /app/src/index.ts && add_score 0.10
grep -q '/api/orders' /app/src/index.ts && add_score 0.05

# ---------------- K8s (0.2) ----------------
grep -q 'containerPort: 3000' /app/k8s-deployment.yaml && add_score 0.05
grep -q "value: '3000'" /app/k8s-deployment.yaml && add_score 0.05
grep -q 'path: /healthz' /app/k8s-deployment.yaml && add_score 0.10

# ---------------- Runtime (0.2) ----------------
cd /app
node dist/index.js >/tmp/app.log 2>&1 &
PID=$!
sleep 2

curl -sf http://localhost:3000/healthz | grep -q '"status":"ok"' && add_score 0.10
curl -sf http://localhost:3000/api/orders | grep -q 'ord-001' && add_score 0.10

kill $PID >/dev/null 2>&1 || true

python3 - <<PY
print(round(min(float("$score"), 1.0), 2))
PY