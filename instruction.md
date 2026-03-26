# Restore the order-service rollout

A recent deployment introduced configuration drift between the application, Docker image, and Kubernetes manifest.

Everything you need is under `/app/`.

Restore the service so that:
- the container builds successfully
- the application runs correctly on port 3000
- the health endpoint responds at `GET /healthz`
- the Kubernetes manifest is consistent with the actual runtime configuration

Do not modify the tests or add new runtime dependencies. Keep the container running as a non-root user.

## Target behavior

After your fix:

- the Docker build from `/app/` succeeds
- the container starts successfully on port `3000`
- `GET /healthz` returns HTTP 200 with `{"status":"ok"}`
- `GET /api/orders` returns HTTP 200 with a JSON array of orders
- the Kubernetes manifest is consistent with the actual container port, environment configuration, and health check path

## Constraints

- Do not modify the tests.
- Do not add new runtime dependencies beyond what is already declared in `package.json`.
- Keep the container running as a non-root user.
- Make your changes in the existing project files.

## Acceptance criteria

Your submission should make the following true:

- `docker build -t order-service /app/` succeeds
- `docker run -d -p 3000:3000 --name order-service order-service` starts successfully
- `curl http://localhost:3000/healthz` returns HTTP 200 with `{"status":"ok"}`
- `curl http://localhost:3000/api/orders` returns HTTP 200 with a JSON array of orders
- `k8s-deployment.yaml` is consistent with the application's port and health endpoint
