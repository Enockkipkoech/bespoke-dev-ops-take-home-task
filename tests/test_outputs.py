from pathlib import Path
import re


def find_app_dir() -> Path:
    for candidate in [
        Path("/app"),
        Path("/workspace"),
        Path("/workspace/default"),
        Path.cwd(),
        Path(__file__).resolve().parent.parent / "environment",
    ]:
        if (candidate / "Dockerfile").exists():
            return candidate
    raise AssertionError("Cannot locate app dir with Dockerfile")


APP = find_app_dir()


def read(path: str) -> str:
    return (APP / path).read_text(encoding="utf-8")


class TestDockerfile:

    def test_env_port_is_3000(self):
        src = read("Dockerfile")
        assert "ENV APP_PORT" not in src, "Dockerfile still sets ENV APP_PORT."
        assert "ENV PORT=3000" in src, "Dockerfile must set ENV PORT=3000."

    def test_expose_is_3000(self):
        src = read("Dockerfile")
        assert "EXPOSE 8080" not in src, "Dockerfile still EXPOSEs 8080."
        assert "EXPOSE 3000" in src, "Dockerfile must EXPOSE 3000."

    def test_multistage_build(self):
        src = read("Dockerfile")
        assert "AS builder" in src
        assert "COPY --from=builder /app/dist ./dist" in src

    def test_omit_dev(self):
        src = read("Dockerfile")
        assert "npm ci --omit=dev" in src

    def test_no_solution_or_tests_copied(self):
        src = read("Dockerfile")
        assert "COPY tests" not in src
        assert "COPY solution" not in src


class TestApplicationSource:

    def test_uses_process_env_port(self):
        src = read("src/index.ts")
        assert "process.env.APP_PORT" not in src, "Still reads APP_PORT."
        assert "process.env.PORT" in src

    def test_port_fallback_3000(self):
        src = read("src/index.ts")
        assert "|| 8080" not in src, "Port fallback still 8080."
        assert re.search(r"process\.env\.PORT.*3000|3000.*process\.env\.PORT", src)

    def test_healthz_route_exists(self):
        src = read("src/index.ts")
        assert "app.get('/healthz'" in src or 'app.get("/healthz"' in src

    def test_health_route_gone(self):
        src = read("src/index.ts")
        assert not re.findall(r"""app\.get\(['"]\/health['"]\s*,""", src)

    def test_orders_router_mounted(self):
        src = read("src/index.ts")
        assert "app.use('/api/orders', ordersRouter)" in src or \
               'app.use("/api/orders", ordersRouter)' in src


class TestKubernetesManifest:

    def test_container_port_3000(self):
        src = read("k8s-deployment.yaml")
        assert "containerPort: 8080" not in src, "containerPort still 8080."
        assert "containerPort: 3000" in src

    def test_port_env_3000(self):
        src = read("k8s-deployment.yaml")
        assert 'value: "3000"' in src or "value: '3000'" in src

    def test_liveness_healthz(self):
        src = read("k8s-deployment.yaml")
        m = re.search(r"livenessProbe:.*?(?=readinessProbe:|$)", src, re.DOTALL)
        assert m and "/healthz" in m.group()

    def test_readiness_healthz(self):
        src = read("k8s-deployment.yaml")
        m = re.search(r"readinessProbe:.*?(?=resources:|$)", src, re.DOTALL)
        assert m and "/healthz" in m.group()

    def test_target_port_3000(self):
        src = read("k8s-deployment.yaml")
        assert "targetPort: 3000" in src

    def test_probe_ports_3000(self):
        src = read("k8s-deployment.yaml")
        assert len(re.findall(r"port:\s*3000", src)) >= 2
