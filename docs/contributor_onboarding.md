# Contributor Onboarding

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

If you are working with ROS2 nodes, source your ROS2 distribution and rebuild:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build
```

## Development Loop

Use focused tests while editing:

```bash
pytest tests/test_memory_inspection_cli.py
ruff check src tests
mypy src
```

Before opening a pull request, run the full release validation command set from
the phase checklist.

## Contribution Expectations

- Keep commits scoped to one behavior or documentation improvement.
- Add tests for new Python behavior.
- Update docs when user-visible commands, examples, or APIs change.
- Avoid committing generated build outputs unless they are explicit release
  artifacts.
