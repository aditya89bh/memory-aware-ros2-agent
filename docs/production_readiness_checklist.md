# Production Readiness Checklist

Use this checklist before publishing or deploying `memory-aware-ros2-agent`.

## Quality Gates

- `pytest` passes locally and in CI.
- `pytest --cov --cov-fail-under=80` meets the coverage gate.
- `ruff check .` passes with strict lint rules.
- `mypy src` passes with strict type checking.
- `python -m build` creates wheel and source distribution artifacts.
- `colcon build` succeeds in a ROS2 workspace.

## Security Gates

- Dependency audit workflow passes.
- CodeQL workflow passes.
- SBOM workflow publishes a CycloneDX artifact.
- `SECURITY.md` is up to date.

## Reliability Gates

- Persistence and recall concurrency tests pass.
- Thread-safety tests pass.
- Memory usage regression tests pass.
- Soak harness completes for the target iteration count.

## Release Gates

- Release artifacts are validated and hashed.
- Documentation validation and dead-link checks pass.
- Operations documentation is current for the deployed environment.
