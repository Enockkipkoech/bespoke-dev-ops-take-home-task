#!/bin/bash
set -euo pipefail
set -x

echo "==> Fixing files using Python to avoid sed permission issues..."

python3 << 'PYEOF'
import re

# Fix src/index.ts
with open('/app/src/index.ts', 'r') as f:
    content = f.read()

content = content.replace('process.env.APP_PORT', 'process.env.PORT')
content = content.replace('|| 8080', '|| 3000')
content = content.replace("app.get('/health',", "app.get('/healthz',")
content = content.replace('app.get("/health",', 'app.get("/healthz",')

with open('/app/src/index.ts', 'w') as f:
    f.write(content)

print("Fixed src/index.ts")

# Fix k8s-deployment.yaml
with open('/app/k8s-deployment.yaml', 'r') as f:
    content = f.read()

content = content.replace('containerPort: 8080', 'containerPort: 3000')

with open('/app/k8s-deployment.yaml', 'w') as f:
    f.write(content)

print("Fixed k8s-deployment.yaml")

# Fix Dockerfile
with open('/app/Dockerfile', 'r') as f:
    content = f.read()

content = content.replace('ENV APP_PORT=8080', 'ENV PORT=3000')
content = content.replace('EXPOSE 8080', 'EXPOSE 3000')

with open('/app/Dockerfile', 'w') as f:
    f.write(content)

print("Fixed Dockerfile")
PYEOF

echo "==> Verification"
grep "process.env.PORT\|app.get(" /app/src/index.ts
grep "containerPort" /app/k8s-deployment.yaml
grep "ENV PORT\|EXPOSE" /app/Dockerfile
echo "==> Done"
