# Restore the order-service rollout

You are the on-call engineer for a small TypeScript order service. A recent containerized deployment is unhealthy: the image builds inconsistently, the service is not reachable on the expected port, and Kubernetes health checks do not succeed.

Everything you need is under `/app/`.

Your job is to restore the service so that it:

- builds successfully with Docker from `/app/`
- starts successfully with `docker run -p 3000:3000 order-service`
- responds successfully on `GET /healthz`
- serves order data successfully on `GET /api/orders`
- has Kubernetes manifest settings that are consistent with the actual container runtime and health endpoint

## Constraints

- Do not modify the tests.
- Do not add new runtime dependencies beyond what is already declared in `package.json`.
- Keep the container running as a non-root user.
- Make your changes in the existing project files.

## Acceptance criteria

Your submission should make the following true:

- `docker build -t order-service /app/` succeeds
- `docker run -d -p 3000:3000 --name order-service order-service` starts and stays healthy
- `curl http://localhost:3000/healthz` returns HTTP 200 with `{"status":"ok"}`
- `curl http://localhost:3000/api/orders` returns HTTP 200 with a JSON array of orders
- `k8s-deployment.yaml` is internally consistent with the application and container runtime
