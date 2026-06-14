# Troubleshooting

## Package Import Fails

Run commands from the repository root or install the package first:

```bash
python -m pip install -e .
```

For local examples, use the scripts in `examples/`; they add `src` to
`PYTHONPATH` automatically.

## ROS2 Commands Are Missing

Source your ROS2 environment before using ROS2 launch or node commands:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
```

Then rebuild with `colcon build` and source `install/setup.bash`.

## JSON Store Looks Empty

Confirm that the same storage path is used for recording and recall. For demos,
prefer absolute paths or keep all commands in the repository root.

## SQLite File Is Locked

Close long-running nodes or CLI sessions that are writing to the same SQLite
database. Retry once the writer has exited.

## CLI Import Or Export Fails

Validate input JSON first:

```bash
python -m json.tool examples/datasets/sample_memory_events.json
```

Use `memory-inspect` on individual event or trace files to confirm their shape.
