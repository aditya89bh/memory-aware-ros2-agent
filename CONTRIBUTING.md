# Contributing

Thanks for your interest in `memory-aware-ros2-agent`.

This project is in its foundation phase. Contributions should keep the package small,
well-tested, and aligned with robot workflow memory: events, task traces, and recall.

## Development Setup

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Before Opening a Pull Request

Run the local checks:

```sh
pytest
ruff check .
mypy src
```

## Contribution Guidelines

- Keep changes focused and reviewable.
- Avoid adding ROS2 runtime code until the relevant phase calls for it.
- Add tests for behavior that affects package contracts.
- Prefer clear, typed Python interfaces over framework-specific shortcuts.
