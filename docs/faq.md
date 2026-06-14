# FAQ

## Do I Need ROS2 To Use The Core Models?

No. The model, persistence, recall, trace intelligence, and CLI utilities are
plain Python. ROS2 is only required for running ROS2 nodes and launch files.

## Which Storage Backend Should I Start With?

Use `InMemoryStore` for tests, `JsonFileStore` for readable local demos,
`EventLogStore` for append-only audit trails, and `SQLiteStore` when you need
indexed local persistence.

## Can I Use The Examples Without Installing The Package?

Yes. The scripts in `examples/` add the local `src` directory to `PYTHONPATH`.
For CLI tools, install the project with `python -m pip install -e .`.

## Are The Sample Datasets Production Data?

No. They are deterministic teaching fixtures intended for demos, docs, and
smoke tests.

## How Should I Validate A Release Candidate?

Run `pytest`, `ruff check .`, `mypy src`, `python -m build`, `colcon build`,
and verify release artifacts with the utilities documented in
`docs/production_readiness_checklist.md`.
