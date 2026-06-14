# Developer Quickstart

## Install Locally

```bash
python -m pip install -e ".[dev]"
```

## Run A Demo

```bash
python examples/basic_memory_recorder.py
python examples/task_replay_demo.py
```

## Try The CLI

```bash
memory-inspect examples/payloads/memory_event.json
memory-export examples/payloads/memory_event.json --output /tmp/memory-bundle.json
memory-import /tmp/memory-bundle.json --output-dir /tmp/memory-records
memory-benchmark --event-count 100 --limit 5
```

## Validate Changes

```bash
pytest
ruff check .
mypy src
python -m build
colcon build
```

## Next Steps

Read `docs/api_reference.md` for module-level APIs, then use
`examples/datasets/` as small inputs for experiments.
